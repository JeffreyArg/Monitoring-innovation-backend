from fastapi import APIRouter

from app.api.v1 import brands_router, localities_router, vehicles_router

api_router = APIRouter()
api_router.include_router(brands_router.router)
api_router.include_router(localities_router.router)
api_router.include_router(vehicles_router.router)
