from pydantic import BaseSettings, Field, AnyHttpUrl
from datetime import timedelta

class Settings(BaseSettings):
    app_name: str = Field("MVPGenie", env="APP_NAME")
    secret_key: str = Field(..., env="SECRET_KEY")
    algorithm: str = Field("HS256", env="ALGORITHM")
    access_token_expire_minutes: int = Field(15, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_token_expire_days: int = Field(30, env="REFRESH_TOKEN_EXPIRE_DAYS")
    database_url: AnyHttpUrl = Field(..., env="DATABASE_URL")
    cors_origins: list[str] = Field(default_factory=lambda: ["https://localhost:3000"], env="CORS_ORIGINS")
    rate_limit: str = Field("100/second", env="RATE_LIMIT")
    log_file: str = Field("app.log", env="LOG_FILE")
    log_level: str = Field("INFO", env="LOG_LEVEL")

settings = Settings()
