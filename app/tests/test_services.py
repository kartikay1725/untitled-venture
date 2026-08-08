import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.models import Base, User, Idea, MVPBlueprint, MVPPackage
from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.services.idea_validation_service import IdeaValidationService
from app.services.mvp_generation_service import MVPGenerationService

DATABASE_URL = "sqlite+aiosqlite:///:memory:"
engine = create_async_engine(DATABASE_URL, echo=False, future=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False, class_=asyncio.Future)

@pytest.fixture(scope="module", autouse=True)
async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.mark.asyncio
async def test_user_registration_and_auth():
    async with async_session_maker() as session:
        user_service = UserService(session)
        auth_service = AuthService(user_service)
        user = await auth_service.register("test@example.com", "Password123")
        assert user.email == "test@example.com"
        auth_user = await auth_service.authenticate("test@example.com", "Password123")
        assert auth_user.id == user.id

@pytest.mark.asyncio
async def test_idea_validation():
    async with async_session_maker() as session:
        user_service = UserService(session)
        user = await user_service.create(User(email="idea@example.com", password_hash="hash"))
        idea_service = IdeaValidationService(session)
        idea = await idea_service.submit_idea(user.id, "A marketable idea for a new app")
        assert idea.validation_score >= 70

@pytest.mark.asyncio
async def test_mvp_generation():
    async with async_session_maker() as session:
        user_service = UserService(session)
        user = await user_service.create(User(email="mvp@example.com", password_hash="hash"))
        idea_service = IdeaValidationService(session)
        idea = await idea_service.submit_idea(user.id, "A marketable idea for a new app")
        mvp_service = MVPGenerationService(session)
        blueprint = await mvp_service.generate_from_idea(user.id, str(idea.id))
        assert blueprint is not None
        assert blueprint.pdf_url
        zip_url = await mvp_service.get_zip_url(user.id, str(blueprint.id))
        assert zip_url
