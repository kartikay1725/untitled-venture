import os
from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    JWT_SECRET: str = Field(..., env="JWT_SECRET")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 60
    OPENAI_API_KEY: str = Field(..., env="OPENAI_API_KEY")
    DEPLOYMENT_SERVICE_API_KEY: str = Field(..., env="DEPLOYMENT_SERVICE_API_KEY")
    SENTRY_DSN: str | None = Field(None, env="SENTRY_DSN")
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()