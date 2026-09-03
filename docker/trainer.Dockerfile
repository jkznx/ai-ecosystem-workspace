FROM pytorch/pytorch:2.13.0-cuda13.0-cudnn9-runtime

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV NVIDIA_VISIBLE_DEVICES=all
ENV NVIDIA_DRIVER_CAPABILITIES=compute,utility

COPY pyproject.toml uv.lock README.md ./
COPY backend ./backend

RUN python -m pip install --no-cache-dir --break-system-packages ".[training]"

RUN python -c \
    "import torch; print(torch.__version__); print(torch.version.cuda)"

CMD ["python", "-m", "arq", "backend.workers.worker_settings.WorkerSettings"]
