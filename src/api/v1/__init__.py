from fastapi import APIRouter

from src.api.v1.places import router as places_router
from src.api.v1.projects import router as projects_router

v1_router = APIRouter(prefix="/api/v1")
v1_router.include_router(projects_router)
v1_router.include_router(places_router)
