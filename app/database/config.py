from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, Field


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


def get_db_settings() -> DatabaseSettings:
    return DatabaseSettings()
