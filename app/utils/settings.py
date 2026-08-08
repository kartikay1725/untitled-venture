from pydantic import BaseSettings, AnyHttpUrl, validator
from typing import List

class Settings(BaseSettings):
    DATABASE_URL: AnyHttpUrl
    JWT_SECRET: str
    JWT_ISSUER: str = "IdeaForge"
    JWT_AUDIENCE: str = "IdeaForgeUsers"
    SESSION_SECRET: str
    CORS_ORIGINS: List[str] = ["https://app.ideaforge.com"]
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    S3_BUCKET_NAME: str
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
