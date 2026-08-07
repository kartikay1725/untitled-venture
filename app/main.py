from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.sessions import SessionMiddleware
import uvicorn
from app.routes import auth, ideas, mvp, deploy
from app.config import settings
from app.database import engine, Base
from app.utils.security_headers import add_security_headers
from app.utils.rate_limiter import limiter, rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
import logging

app = FastAPI(title="IdeaForge API", version="1.0.0")

# Middleware
app.add_middleware(HTTPSRedirectMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key=settings.SESSION_SECRET)
app.add_middleware(BaseHTTPMiddleware, dispatch=add_security_headers)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)

# Routes
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(ideas.router, prefix="/api/ideas", tags=["ideas"])
app.include_router(mvp.router, prefix="/api/mvp", tags=["mvp"])
app.include_router(deploy.router, prefix="/api/deploy", tags=["deploy"])

# Startup event
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Error handlers
@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    logging.exception("Unhandled exception")
    return JSONResponse(status_code=500, content={"detail":"Internal Server Error"})

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
