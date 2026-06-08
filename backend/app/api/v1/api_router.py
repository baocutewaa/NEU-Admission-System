from fastapi import APIRouter
from app.api.v1.endpoints import analytics, students, ai_chat

api_router = APIRouter()
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
api_router.include_router(students.router, prefix="/students", tags=["students"])
api_router.include_router(ai_chat.router, prefix="/chat", tags=["chat"])
