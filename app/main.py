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
        "https://jeffreyarg.github.io",
        "https://jeffreyarg.github.io/Monitoring-innovation-frontend",
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET","POST","PUT","PATCH","DELETE","OPTIONS"],
    allow_headers=["*"],
    expose_headers=["Content-Range","X-Total-Count"],
    max_age=86400,
)

app.include_router(api_router, prefix="/api/v1")
