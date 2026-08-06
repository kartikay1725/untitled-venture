from fastapi import FastAPI
from .api.routes import auth, ideas, blueprints
from .database.engine import init_db
from prometheus_fastapi_instrumentator import Instrumentator
import logging

logging.basicConfig(level=logging.INFO)
app = FastAPI(title="MVPGenie API")

@app.on_event("startup")
async def startup():
    await init_db()

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(ideas.router, prefix="/api/ideas", tags=["ideas"])
app.include_router(blueprints.router, prefix="/api/blueprints", tags=["blueprints"])

@app.get("/health")
async def health():
    return {"status": "ok"}

instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app, endpoint="/metrics")
