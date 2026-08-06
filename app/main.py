import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from starlette_limiter import Limiter, _rate_limit_exceeded_handler
from starlette_limiter.depends import RateLimiter
from .config import settings
from .auth import router as auth_router
from .ideas import router as ideas_router
from .blueprints import router as blueprints_router
from .database import engine
from sqlmodel import SQLModel

# Setup logging
logging.basicConfig(filename=settings.log_file, level=getattr(logging, settings.log_level), format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title=settings.app_name)

# Security headers middleware
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response: Response = await call_next(request)
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains; preload"
        return response

app.add_middleware(SecurityHeadersMiddleware)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# HTTPS redirect
app.add_middleware(HTTPSRedirectMiddleware)

# Rate limiting
limiter = Limiter(key_func=lambda request: request.client.host, default_limits=[settings.rate_limit])
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)

# Include routers
app.include_router(auth_router)
app.include_router(ideas_router)
app.include_router(blueprints_router)

# Database initialization
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    logger.info("Database tables created")
