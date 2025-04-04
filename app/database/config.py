from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, Field, AmqpDsn
from typing import Optional

class DatabaseSettings(BaseSettings):
    POSTGRES_USER: str = Field(..., alias="DB_USER")
    POSTGRES_PASSWORD: str = Field(..., alias="DB_PASSWORD")
    POSTGRES_DB: str = Field(..., alias="DB_NAME")
    POSTGRES_HOST: str = Field("database", alias="DB_HOST")
    POSTGRES_PORT: int = Field(5432, alias="DB_PORT")

    @property
    def DATABASE_URL(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=str(self.POSTGRES_PORT),
            path=self.POSTGRES_DB,
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False
    )

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

def get_db_settings() -> DatabaseSettings:
    return DatabaseSettings()

def get_ml_settings() -> MLServiceSettings:
    return MLServiceSettings()

def get_rabbitmq_settings() -> RabbitMQSettings:
    return RabbitMQSettings()

def get_app_settings() -> AppSettings:
    return AppSettings()
