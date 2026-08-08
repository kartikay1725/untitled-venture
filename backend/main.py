from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import os
from .app.api import auth, ideas, mvp
from .app.db import SessionLocal, engine
from .app.models import Base
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="IdeaForge API", version="1.0.0")

# CORS
origins = os.getenv("CORS_ALLOWLIST", "").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if origins != [''] else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security headers middleware
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self'; style-src 'self';"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        return response

app.add_middleware(SecurityHeadersMiddleware)

# Routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(ideas.router, prefix="/api/ideas", tags=["ideas"])
app.include_router(mvp.router, prefix="/api/mvp", tags=["mvp"])

# Dependency
@app.middleware("http")
async def db_session_middleware(request, call_next):
    request.state.db = SessionLocal()
    try:
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response

# Exception handlers
@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    logger.exception("Unhandled exception")
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})