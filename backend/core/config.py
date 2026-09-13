from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    APP_NAME: str = "ai-ecosystem-backend"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    TRAINER_QUEUE_NAME: str = "trainer"
    TRAINER_JOB_TIMEOUT_SECONDS: int = 14400
    TRAINER_RESULT_TTL_SECONDS: int = 604800
    INFERENCE_QUEUE_NAME: str = "inference"
    INFERENCE_JOB_TIMEOUT_SECONDS: int = 600
    INFERENCE_RESULT_TTL_SECONDS: int = 86400
    INFERENCE_API_WAIT_SECONDS: int = 300

    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "label_studio"

    MINIO_ENDPOINT: str = "localhost:9000"
    MINIO_ACCESS_KEY: str = "minioadmin"
    MINIO_SECRET_KEY: str = "minioadmin"
    MINIO_BUCKET: str = "selfie-photos"
    MINIO_SECURE: bool = False
    MINIO_DATASET_BUCKET: str = "training-datasets"
    MINIO_MODEL_BUCKET: str = "trained-models"
    MINIO_LOG_BUCKET: str = "training-logs"

    TRAINING_LOG_DIR: str = "logs/training-logs"

    MLFLOW_TRACKING_URI: str = "http://localhost:5000"
    MLFLOW_EXPERIMENT_NAME: str = "token-classification"
    MLFLOW_ARTIFACT_BUCKET: str = "mlflow-artifacts"
    MLFLOW_REGISTERED_MODEL_ALIAS: str = "champion"

    # Observability
    OBSERVABILITY_ENABLED: bool = True
    OTEL_SERVICE_NAME: str = "ai-ecosystem-service"
    OTEL_EXPORTER_OTLP_ENDPOINT: str = "http://localhost:4317"
    OTEL_EXPORTER_OTLP_INSECURE: bool = True
    OTEL_EXCLUDED_URLS: str = "/metrics,/health,/health/ready,/health/observability"
    PROMETHEUS_METRICS_PATH: str = "/metrics"
    TRAINER_METRICS_PORT: int = 9101
    INFERENCE_METRICS_PORT: int = 9102
    OTEL_COLLECTOR_HEALTH_URL: str = "http://localhost:13133/"
    PROMETHEUS_URL: str = "http://localhost:9090"
    LOKI_URL: str = "http://localhost:3100"
    TEMPO_URL: str = "http://localhost:3200"
    GRAFANA_URL: str = "http://localhost:3000"

    # JWT Setting
    JWT_SECRET_KEY: str = "change-me-in-.env"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # admin init
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "admin"  # ควรเปลี่ยนใน .env เมื่อใช้งานจริง

    @property
    def POSTGRES_DSN(self) -> str:
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    LABEL_STUDIO_URL: str = "http://localhost:8080"
    LABEL_STUDIO_API_KEY: str = ""


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
