FROM pytorch/pytorch:2.13.0-cuda13.0-cudnn9-runtime

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock README.md ./

RUN uv export --quiet \
    --locked \
    --no-dev \
    --no-emit-project \
    --extra training \
    --output-file /tmp/requirements.txt \
    && uv pip install \
    --system \
    --break-system-packages \
    --requirements /tmp/requirements.txt

COPY backend ./backend

RUN python -c \
    "import torch; print(torch.__version__); print(torch.version.cuda)"

CMD ["python", "-m", "arq", "backend.workers.worker_settings.WorkerSettings"]
