import os
import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from prometheus_fastapi_instrumentator import Instrumentator
from .api.routes import ideas
from .api.utils.env import Settings
from .api.utils.logger import get_logger, add_correlation_id

settings = Settings()
logger = get_logger()

app = FastAPI(title="IdeaForge API", version="1.0.0")

app.middleware("http")(add_correlation_id)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(ideas.router, prefix="/api/ideas")

@app.get("/health", tags=["Health"])
async def health() -> JSONResponse:
    return JSONResponse(content={"status": "ok"})

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    logger.error(f"HTTP error: {exc.detail}")
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

@app.on_event("startup")
async def startup_event():
    logger.info("Application startup: validating environment")
    settings.validate()

Instrumentator().instrument(app).expose(app, endpoint="/metrics")