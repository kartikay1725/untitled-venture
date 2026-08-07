from pydantic import BaseSettings, AnyHttpUrl, validator
from typing import List

class Settings(BaseSettings):
    DATABASE_URL: AnyHttpUrl
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    SESSION_SECRET: str
    CORS_ORIGINS: List[AnyHttpUrl] = ["https://localhost:3000"]
    OPENAI_API_KEY: str
    DEPLOYMENT_SERVICE_API_KEY: str

    @validator("CORS_ORIGINS", pre=True)
    def split_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
