from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import  AmqpDsn
from typing import Optional

class Settings(BaseSettings):
    RABBITMQ_QUEUE: str = "prediction_tasks"

settings = Settings()

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
