import os
from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    JWT_SECRET: str = Field(..., env="JWT_SECRET")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    AWS_ACCESS_KEY_ID: str = Field(..., env="AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY: str = Field(..., env="AWS_SECRET_ACCESS_KEY")
    S3_BUCKET_NAME: str = Field(..., env="S3_BUCKET_NAME")
    STORAGE_PATH: str = Field("./storage", env="STORAGE_PATH")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()