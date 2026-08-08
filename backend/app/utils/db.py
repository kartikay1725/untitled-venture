import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_async_engine(DATABASE_URL, echo=False, future=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session

async def get_current_user(token: str = Depends(lambda: None)):
    from app.utils.security import decode_token
    payload = decode_token(token)
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid authentication")
    session = await async_session_maker()
    user_service = UserService(session)
    user = await user_service.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user