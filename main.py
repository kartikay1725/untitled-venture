from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import logging, os, uuid
from datetime import datetime
from .models import User, Idea, Blueprint
from .services import ValidationService, BlueprintService
from .ai import AIClient

# Logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("mvpgenie")

# Environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CHROMA_URL = os.getenv("CHROMA_URL")

# Database setup
engine = create_async_engine(DATABASE_URL, echo=False)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# FastAPI app
app = FastAPI(title="MVPGenie API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Dependency
async def get_db():
    async with async_session() as session:
        yield session

# AI client singleton
ai_client = AIClient(openai_key=OPENAI_API_KEY, chroma_url=CHROMA_URL)

# Pydantic schemas
class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class IdeaRequest(BaseModel):
    title: str = Field(..., max_length=200)
    description: str

class ValidationResponse(BaseModel):
    validation_score: float
    validation_feedback: dict
    status: str

class BlueprintRequest(BaseModel):
    idea_id: uuid.UUID
    scope: str

class BlueprintResponse(BaseModel):
    features: list
    timeline: dict

# Auth routes
@app.post("/auth/register")
async def register(req: RegisterRequest, db: AsyncSession = Depends(get_db)):
    service = ValidationService(db)
    user = await service.create_user(req.email, req.password)
    return {"id": str(user.id), "email": user.email}

@app.post("/auth/login")
async def login(form: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    service = ValidationService(db)
    token = await service.authenticate(form.username, form.password)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return {"access_token": token, "token_type": "bearer"}

# Idea routes
@app.post("/ideas", status_code=status.HTTP_201_CREATED)
async def submit_idea(req: IdeaRequest, token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    service = ValidationService(db)
    idea = await service.submit_idea(token, req.title, req.description)
    return {"idea_id": str(idea.id), "status": idea.status}

@app.get("/ideas/{idea_id}/validation", response_model=ValidationResponse)
async def get_validation(idea_id: uuid.UUID, token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    service = ValidationService(db)
    result = await service.get_validation(token, idea_id)
    if not result:
        raise HTTPException(status_code=404, detail="Idea not found or not validated")
    return result

# Blueprint routes
@app.post("/blueprints", status_code=status.HTTP_201_CREATED)
async def generate_blueprint(req: BlueprintRequest, token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    service = BlueprintService(db, ai_client)
    blueprint = await service.create_blueprint(token, req.idea_id, req.scope)
    return {"blueprint_id": str(blueprint.id)}

@app.get("/blueprints/{blueprint_id}", response_model=BlueprintResponse)
async def get_blueprint(blueprint_id: uuid.UUID, token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    service = BlueprintService(db, ai_client)
    blueprint = await service.get_blueprint(token, blueprint_id)
    if not blueprint:
        raise HTTPException(status_code=404, detail="Blueprint not found")
    return {"features": blueprint.features, "timeline": blueprint.timeline}

# Startup event: create tables
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(User.metadata.create_all)
        await conn.run_sync(Idea.metadata.create_all)
        await conn.run_sync(Blueprint.metadata.create_all)

# Graceful shutdown
@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()
