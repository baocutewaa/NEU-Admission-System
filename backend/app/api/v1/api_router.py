from fastapi import APIRouter
from app.api.v1.endpoints import analytics, students

api_router = APIRouter()
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
api_router.include_router(students.router, prefix="/students", tags=["students"])
