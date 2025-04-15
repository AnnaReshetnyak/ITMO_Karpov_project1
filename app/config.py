from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import  AmqpDsn
from typing import Optional
import logging


class Settings(BaseSettings):
    RABBITMQ_URL: str = "amqp://admin:securepassword@rabbitmq-broker/"
    RABBITMQ_QUEUE: str = "prediction_tasks"


settings = Settings()

def configure_logging():
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO
    )

class DatabaseSettings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = "database"
    POSTGRES_PORT: int = 5432

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False  # Игнорировать регистр переменных
    )

def get_settings() -> DatabaseSettings:
    return DatabaseSettings()


class MLServiceSettings(BaseSettings):
    ML_API_KEY: Optional[str] = None
    ML_MODEL_ENDPOINT: str = "https://api.ml-service.com/v1/predict"
    PREDICTION_HISTORY_ENABLED: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="ML_"
    )

class RabbitMQSettings(BaseSettings):
    RABBITMQ_USER: str = "guest"
    RABBITMQ_PASS: str = "guest"
    RABBITMQ_HOST: str = "rabbitmq"
    RABBITMQ_PORT: int = 5672

    @property
    def AMQP_URL(self) -> AmqpDsn:
        return AmqpDsn.build(
            scheme="amqp",
            username=self.RABBITMQ_USER,
            password=self.RABBITMQ_PASS,
            host=self.RABBITMQ_HOST,
            port=str(self.RABBITMQ_PORT)
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="RABBITMQ_"
    )

class AppSettings(BaseSettings):
    DEBUG: bool = False
    SECRET_KEY: str = "your-secret-key-here"
    TOKEN_EXPIRE_MINUTES: int = 1440  # 24 часа

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="APP_"
    )

def get_ml_settings() -> MLServiceSettings:
    return MLServiceSettings()

def get_rabbitmq_settings() -> RabbitMQSettings:
    return RabbitMQSettings()

def get_app_settings() -> AppSettings:
    return AppSettings()
