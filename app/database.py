from sqlmodel import SQLModel, create_engine, Session
from .config import settings

engine = create_engine(settings.database_url, echo=False, future=True)

def get_session() -> Session:
    return Session(engine, autoflush=False, autocommit=False)
