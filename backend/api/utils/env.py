from pydantic import BaseSettings, AnyHttpUrl, validator
from typing import List

class Settings(BaseSettings):
    DATABASE_URL: AnyHttpUrl
    JWT_SECRET: str
    OPENAI_API_KEY: str
    DEPLOYMENT_SERVICE_API_KEY: str
    CORS_ORIGINS: List[str] = ["https://example.com"]
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
    def validate(self):
        missing = []
        for field in ["DATABASE_URL", "JWT_SECRET", "OPENAI_API_KEY", "DEPLOYMENT_SERVICE_API_KEY"]:
            if not getattr(self, field):
                missing.append(field)
        if missing:
            raise RuntimeError(f"Missing required environment variables: {', '.join(missing)}")