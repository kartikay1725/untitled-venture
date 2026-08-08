"""FastAPI application entry point.

This module sets up the FastAPI app, includes routers for authentication, idea
submission/validation, and MVP generation, and configures the database session
and logging.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import logging

from app.api import auth, ideas, mvp
from app.database import engine, Base, get_db

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="IdeaForge API", description="Validate ideas and generate MVPs.")

# CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app.ideaforge.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(ideas.router, prefix="/api/ideas", tags=["ideas"])
app.include_router(mvp.router, prefix="/api/mvp", tags=["mvp"])

# Exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    logger.warning("Validation error: %s", exc)
    return JSONResponse(status_code=422, content={"detail": exc.errors()})

# Create database tables on startup
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created.")

# Dependency for DB session
@app.middleware("http")
async def db_session_middleware(request, call_next):
    request.state.db = get_db()
    response = await call_next(request)
    return response

# Graceful shutdown
@app.on_event("shutdown")
async def on_shutdown():
    await engine.dispose()
    logger.info("Database connection closed.")