from __future__ import annotations

import json
import logging
import tarfile
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import evaluate
import numpy as np
import torch
from datasets import DatasetDict, load_from_disk
from minio import Minio
from transformers import (
    AutoModelForTokenClassification,
    AutoTokenizer,
    DataCollatorForTokenClassification,
    Trainer,
    TrainingArguments,
)

from backend.api.schemas.training import TrainingRequest
from backend.core.config import settings
from backend.libs.minio_client import (
    ensure_bucket,
    get_minio_client,
)


def create_job_logger(
    job_id: str,
    log_path: Path,
) -> logging.Logger:
    logger = logging.getLogger(f"trainer.{job_id}")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    logger.handlers.clear()

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    file_handler = logging.FileHandler(
        log_path,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def flush_logger(logger: logging.Logger) -> None:
    for handler in logger.handlers:
        handler.flush()


def close_logger(logger: logging.Logger) -> None:
    for handler in list(logger.handlers):
        handler.flush()
        handler.close()
        logger.removeHandler(handler)


def safe_extract_archive(
    archive_path: Path,
    destination: Path,
) -> None:
    destination = destination.resolve()

    with tarfile.open(archive_path, mode="r:gz") as archive:
        for member in archive.getmembers():
            member_path = (
                destination / member.name
            ).resolve()

            if (
                member_path != destination
                and destination not in member_path.parents
            ):
                raise ValueError(
                    f"Unsafe archive member: {member.name}"
                )

        archive.extractall(destination)


def tokenize_and_align_labels(
    examples: dict[str, Any],
    tokenizer: Any,
) -> dict[str, Any]:
    tokenized_inputs = tokenizer(
        examples["tokens"],
        truncation=True,
        is_split_into_words=True,
    )

    aligned_labels = []

    for batch_index, labels in enumerate(
        examples["ner_tags"]
    ):
        word_ids = tokenized_inputs.word_ids(
            batch_index=batch_index
        )

        previous_word_id = None
        label_ids = []

        for word_id in word_ids:
            if word_id is None:
                label_ids.append(-100)
            elif word_id != previous_word_id:
                label_ids.append(labels[word_id])
            else:
                label_ids.append(-100)

            previous_word_id = word_id

        aligned_labels.append(label_ids)

    tokenized_inputs["labels"] = aligned_labels
    return tokenized_inputs


def create_compute_metrics(label_names: list[str]):
    metric = evaluate.load("seqeval")

    def compute_metrics(
        evaluation_prediction: Any,
    ) -> dict[str, float]:
        logits, labels = evaluation_prediction
        predictions = np.argmax(logits, axis=-1)

        true_predictions = []
        true_labels = []

        for prediction_row, label_row in zip(
            predictions,
            labels,
        ):
            prediction_labels = []
            expected_labels = []

            for prediction, label in zip(
                prediction_row,
                label_row,
            ):
                if label == -100:
                    continue

                prediction_labels.append(
                    label_names[int(prediction)]
                )
                expected_labels.append(
                    label_names[int(label)]
                )

            true_predictions.append(prediction_labels)
            true_labels.append(expected_labels)

        result = metric.compute(
            predictions=true_predictions,
            references=true_labels,
        )

        return {
            "precision": float(
                result["overall_precision"]
            ),
            "recall": float(
                result["overall_recall"]
            ),
            "f1": float(result["overall_f1"]),
            "accuracy": float(
                result["overall_accuracy"]
            ),
        }

    return compute_metrics


def upload_directory(
    client: Minio,
    bucket_name: str,
    local_directory: Path,
    object_prefix: str,
) -> None:
    for local_path in local_directory.rglob("*"):
        if not local_path.is_file():
            continue

        relative_path = local_path.relative_to(
            local_directory
        )

        object_name = (
            f"{object_prefix}/"
            f"{relative_path.as_posix()}"
        )

        client.fput_object(
            bucket_name=bucket_name,
            object_name=object_name,
            file_path=str(local_path),
            content_type="application/octet-stream",
        )


def json_safe_metrics(
    metrics: dict[str, Any],
) -> dict[str, Any]:
    return json.loads(
        json.dumps(metrics, default=float)
    )


async def train_token_classifier(
    ctx: dict[str, Any],
    payload: dict[str, Any],
) -> dict[str, Any]:
    job_id = str(ctx["job_id"])
    request = TrainingRequest.model_validate(
        payload,
        context={"allow_past_start_at": True},
    )

    log_directory = Path(settings.TRAINING_LOG_DIR)
    log_directory.mkdir(parents=True, exist_ok=True)

    log_path = log_directory / f"{job_id}.log"
    logger = create_job_logger(job_id, log_path)

    log_object = f"jobs/{job_id}/training.log"
    client = get_minio_client()

    try:
        logger.info("Training job started")
        logger.info("Job ID: %s", job_id)
        logger.info(
            "Scheduled time: %s",
            request.start_at.isoformat(),
        )
        logger.info(
            "Dataset: %s/%s",
            request.dataset_bucket,
            request.dataset_object,
        )
        logger.info(
            "Base model: %s",
            request.base_model,
        )
        logger.info(
            "Output model name: %s",
            request.model_name,
        )
        logger.info(
            "PyTorch version: %s",
            torch.__version__,
        )
        logger.info(
            "CUDA runtime: %s",
            torch.version.cuda,
        )
        logger.info(
            "CUDA available: %s",
            torch.cuda.is_available(),
        )

        if not torch.cuda.is_available():
            raise RuntimeError(
                "CUDA is not available inside trainer container"
            )

        gpu_name = torch.cuda.get_device_name(0)
        gpu_memory_gb = (
            torch.cuda.get_device_properties(0).total_memory
            / 1024**3
        )

        logger.info("GPU: %s", gpu_name)
        logger.info(
            "GPU memory: %.2f GB",
            gpu_memory_gb,
        )

        with tempfile.TemporaryDirectory(
            prefix=f"{job_id}-"
        ) as temporary_directory:
            work_root = Path(temporary_directory)

            archive_path = (
                work_root / "dataset.tar.gz"
            )
            extract_directory = (
                work_root / "dataset"
            )
            model_directory = (
                work_root / "model"
            )

            extract_directory.mkdir(
                parents=True,
                exist_ok=True,
            )
            model_directory.mkdir(
                parents=True,
                exist_ok=True,
            )

            logger.info(
                "Downloading Dataset from MinIO"
            )

            client.fget_object(
                bucket_name=request.dataset_bucket,
                object_name=request.dataset_object,
                file_path=str(archive_path),
            )

            logger.info("Extracting Dataset archive")

            safe_extract_archive(
                archive_path=archive_path,
                destination=extract_directory,
            )

            dataset_path = (
                extract_directory
                / request.dataset_name
            )

            if not dataset_path.exists():
                raise FileNotFoundError(
                    f"Dataset directory not found: "
                    f"{dataset_path}"
                )

            logger.info(
                "Loading Dataset from %s",
                dataset_path,
            )

            dataset: DatasetDict = load_from_disk(
                str(dataset_path)
            )

            if "train" not in dataset:
                raise ValueError(
                    "Dataset does not contain train split"
                )

            if "validation" not in dataset:
                raise ValueError(
                    "Dataset does not contain validation split"
                )

            label_feature = dataset[
                "train"
            ].features["ner_tags"].feature

            label_names = list(label_feature.names)

            id_to_label = {
                index: label
                for index, label in enumerate(label_names)
            }

            label_to_id = {
                label: index
                for index, label in id_to_label.items()
            }

            logger.info(
                "Loading tokenizer: %s",
                request.base_model,
            )

            tokenizer = AutoTokenizer.from_pretrained(
                request.base_model
            )

            logger.info(
                "Tokenizing and aligning labels"
            )

            tokenized_dataset = dataset.map(
                lambda examples: tokenize_and_align_labels(
                    examples,
                    tokenizer,
                ),
                batched=True,
                remove_columns=dataset[
                    "train"
                ].column_names,
            )

            logger.info(
                "Loading model: %s",
                request.base_model,
            )

            model = (
                AutoModelForTokenClassification
                .from_pretrained(
                    request.base_model,
                    num_labels=len(label_names),
                    id2label=id_to_label,
                    label2id=label_to_id,
                )
            )

            data_collator = (
                DataCollatorForTokenClassification(
                    tokenizer=tokenizer
                )
            )

            training_arguments = TrainingArguments(
                output_dir=str(model_directory),
                num_train_epochs=request.epochs,
                learning_rate=request.learning_rate,
                per_device_train_batch_size=(
                    request.batch_size
                ),
                per_device_eval_batch_size=(
                    request.batch_size
                ),
                gradient_accumulation_steps=2,
                fp16=True,
                eval_strategy="epoch",
                save_strategy="epoch",
                logging_strategy="steps",
                logging_steps=10,
                save_total_limit=2,
                load_best_model_at_end=True,
                metric_for_best_model="f1",
                greater_is_better=True,
                dataloader_pin_memory=True,
                report_to=[],
            )

            trainer = Trainer(
                model=model,
                args=training_arguments,
                train_dataset=tokenized_dataset[
                    "train"
                ],
                eval_dataset=tokenized_dataset[
                    "validation"
                ],
                data_collator=data_collator,
                processing_class=tokenizer,
                compute_metrics=create_compute_metrics(
                    label_names
                ),
            )

            logger.info("Model training started")

            training_result = trainer.train()

            logger.info("Model evaluation started")

            evaluation_metrics = trainer.evaluate()

            logger.info("Saving model and tokenizer")

            trainer.save_model(str(model_directory))
            trainer.save_state()

            tokenizer.save_pretrained(
                str(model_directory)
            )

            training_metrics = json_safe_metrics(
                training_result.metrics
            )
            evaluation_metrics = json_safe_metrics(
                evaluation_metrics
            )

            metrics_payload = {
                "training": training_metrics,
                "evaluation": evaluation_metrics,
            }

            metrics_path = (
                model_directory / "metrics.json"
            )

            metrics_path.write_text(
                json.dumps(
                    metrics_payload,
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )

            completed_at = datetime.now(
                timezone.utc
            )

            model_prefix = (
                f"models/{request.model_name}/"
                f"{completed_at.strftime('%Y%m%dT%H%M%SZ')}/"
                f"{job_id}"
            )

            manifest = {
                "job_id": job_id,
                "queue_name": (
                    settings.TRAINER_QUEUE_NAME
                ),
                "model_name": request.model_name,
                "base_model": request.base_model,
                "dataset_bucket": (
                    request.dataset_bucket
                ),
                "dataset_object": (
                    request.dataset_object
                ),
                "epochs": request.epochs,
                "batch_size": request.batch_size,
                "learning_rate": (
                    request.learning_rate
                ),
                "pytorch_version": torch.__version__,
                "cuda_version": torch.version.cuda,
                "gpu": gpu_name,
                "gpu_memory_gb": round(
                    gpu_memory_gb,
                    2,
                ),
                "completed_at": (
                    completed_at.isoformat()
                ),
                "metrics": evaluation_metrics,
            }

            manifest_path = (
                model_directory / "manifest.json"
            )

            manifest_path.write_text(
                json.dumps(
                    manifest,
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )

            logger.info(
                "Uploading model to MinIO: %s/%s",
                settings.MINIO_MODEL_BUCKET,
                model_prefix,
            )

            ensure_bucket(
                settings.MINIO_MODEL_BUCKET
            )

            upload_directory(
                client=client,
                bucket_name=(
                    settings.MINIO_MODEL_BUCKET
                ),
                local_directory=model_directory,
                object_prefix=model_prefix,
            )

            logger.info(
                "Training completed successfully"
            )

            return {
                "job_id": job_id,
                "status": "complete",
                "model_bucket": (
                    settings.MINIO_MODEL_BUCKET
                ),
                "model_prefix": model_prefix,
                "log_bucket": (
                    settings.MINIO_LOG_BUCKET
                ),
                "log_object": log_object,
                "metrics": evaluation_metrics,
            }

    except Exception:
        logger.exception("Training job failed")
        raise

    finally:
        logger.info("Training worker cleanup started")
        flush_logger(logger)

        try:
            ensure_bucket(settings.MINIO_LOG_BUCKET)

            client.fput_object(
                bucket_name=settings.MINIO_LOG_BUCKET,
                object_name=log_object,
                file_path=str(log_path),
                content_type="text/plain",
            )

            logger.info(
                "Training log uploaded to %s/%s",
                settings.MINIO_LOG_BUCKET,
                log_object,
            )
        except Exception:
            logger.exception(
                "Could not upload training log"
            )

        flush_logger(logger)
        close_logger(logger)

        if torch.cuda.is_available():
            torch.cuda.empty_cache()
