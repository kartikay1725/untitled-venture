from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..db.database import get_session

router = APIRouter()

@router.get("/health")
async def health(session: AsyncSession = Depends(get_session)):
    try:
        await session.execute("SELECT 1")
        db_status = "ok"
    except Exception:
        db_status = "fail"
    return {"status": "ok", "db": db_status}