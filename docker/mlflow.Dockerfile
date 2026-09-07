FROM python:3.11-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

RUN python -m pip install \
    "mlflow==3.15.0" \
    "psycopg2-binary>=2.9.12" \
    "boto3>=1.42.0"

EXPOSE 5000

CMD ["mlflow", "server", "--host", "0.0.0.0", "--port", "5000"]
