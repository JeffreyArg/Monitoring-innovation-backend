import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import api_router

app = FastAPI(title="Prueba Técnica API", version="1.0.0")

origins_env = os.getenv("CORS_ORIGINS", "")
allow_origins = [o.strip() for o in origins_env.split(",") if o.strip()]

allow_origin_regex = os.getenv("CORS_ORIGIN_REGEX", None)

if not allow_origins and not allow_origin_regex:
    allow_origins = [
        "http://localhost:4200",
        "http://127.0.0.1:4200",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_origin_regex=allow_origin_regex,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")
