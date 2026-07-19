from functools import lru_cache
from pydantic_settings  import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    APP_NAME: str = "ai-ecosystem-backend"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "label_studio"

    @property
    def POSTGRES_DSN(self) -> str:
        return (f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
                f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}")

    LABEL_STUDIO_URL: str = "http://localhost:8080"
    LABEL_STUDIO_API_KEY: str = ""

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()