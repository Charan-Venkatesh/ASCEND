from fastapi import APIRouter

from app.api.v1 import auth, dashboard, mentor, missions, roadmaps

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(roadmaps.router, prefix="/roadmaps", tags=["roadmaps"])
api_router.include_router(missions.router, prefix="/missions", tags=["missions"])
api_router.include_router(mentor.router, prefix="/mentor", tags=["mentor"])
