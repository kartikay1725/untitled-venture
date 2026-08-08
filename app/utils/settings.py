from pydantic import BaseSettings, PostgresDsn
class Settings(BaseSettings):
    DATABASE_URL: PostgresDsn
    JWT_SECRET: str
    class Config:
        env_file = ".env"