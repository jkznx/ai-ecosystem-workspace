"""Download CoNLL-2003 and upload it to MinIO as a tar.gz archive."""

from __future__ import annotations

import os
import tarfile
import tempfile
from pathlib import Path

from datasets import load_dataset
from dotenv import load_dotenv
from minio import Minio
from minio.error import S3Error


DATASET_NAME = "BramVanroy/conll2003"
DATASET_DIRECTORY_NAME = "conll2003"
DATASET_VERSION = "v1"

BUCKET_NAME = "training-datasets"
OBJECT_KEY = "datasets/conll2003/v1/conll2003.tar.gz"


def read_required_environment(name: str) -> str:
    value = os.getenv(name)

    if value is None or not value.strip():
        raise RuntimeError(f"Missing required environment variable: {name}")

    return value.strip()


def read_boolean_environment(name: str, default: bool = False) -> bool:
    value = os.getenv(name)

    if value is None:
        return default

    return value.strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }


def create_minio_client() -> Minio:
    return Minio(
        endpoint=os.getenv("MINIO_ENDPOINT", "localhost:9000"),
        access_key=read_required_environment("MINIO_ACCESS_KEY"),
        secret_key=read_required_environment("MINIO_SECRET_KEY"),
        secure=read_boolean_environment("MINIO_SECURE"),
    )


def ensure_bucket(client: Minio, bucket_name: str) -> None:
    if client.bucket_exists(bucket_name):
        return

    try:
        client.make_bucket(bucket_name)
    except S3Error as error:
        if error.code not in {
            "BucketAlreadyExists",
            "BucketAlreadyOwnedByYou",
        }:
            raise


def create_archive(source_directory: Path, archive_path: Path) -> None:
    with tarfile.open(archive_path, mode="w:gz") as archive:
        archive.add(
            source_directory,
            arcname=source_directory.name,
        )


def main() -> None:
    load_dotenv()

    with tempfile.TemporaryDirectory(
        prefix="conll2003-upload-"
    ) as temporary_directory:
        temporary_root = Path(temporary_directory)
        dataset_directory = temporary_root / DATASET_DIRECTORY_NAME
        archive_path = temporary_root / "conll2003.tar.gz"

        print(f"Downloading {DATASET_NAME} from Hugging Face...")

        dataset = load_dataset(DATASET_NAME)

        print(f"Saving DatasetDict to {dataset_directory}...")

        dataset.save_to_disk(str(dataset_directory))

        print(f"Creating archive {archive_path}...")

        create_archive(
            source_directory=dataset_directory,
            archive_path=archive_path,
        )

        print("Connecting to MinIO...")

        client = create_minio_client()

        print(f"Creating bucket {BUCKET_NAME} when required...")

        ensure_bucket(client, BUCKET_NAME)

        print(f"Uploading {OBJECT_KEY}...")

        result = client.fput_object(
            bucket_name=BUCKET_NAME,
            object_name=OBJECT_KEY,
            file_path=str(archive_path),
            content_type="application/gzip",
            metadata={
                "dataset-name": "conll2003",
                "dataset-version": DATASET_VERSION,
                "source": "hugging-face",
            },
        )

        print("Upload completed")
        print(f"Bucket: {BUCKET_NAME}")
        print(f"Object: {OBJECT_KEY}")
        print(f"ETag: {result.etag}")

        if result.version_id:
            print(f"Version ID: {result.version_id}")

    print("Temporary files removed")


if __name__ == "__main__":
    try:
        main()
    except (OSError, RuntimeError, S3Error) as error:
        raise SystemExit(f"Dataset upload failed: {error}") from error
