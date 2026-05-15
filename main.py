from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.endpoints import router
from src.core.settings import config

app = FastAPI(title=config.application_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")
