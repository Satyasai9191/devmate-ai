from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.conversations import (
    router as conversations_router,
)
from app.core.config import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()

    print(f"Starting {settings.app_name}")
    print(f"Environment: {settings.environment}")

    yield

    print(f"Stopping {settings.app_name}")


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Production-oriented local AI agent platform.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    conversations_router,
    prefix=settings.api_prefix,
)


@app.get("/")
async def root():
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "running",
    }


@app.get("/api/health")
async def root_health():
    return {
        "status": "healthy",
        "service": "backend",
        "version": settings.app_version,
    }