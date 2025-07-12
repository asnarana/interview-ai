from fastapi import APIRouter
from app.api.v1.endpoints import interviews
api_router = APIRouter()

# include all endpoint routers with their prefixes and tags
#api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(interviews.router, prefix="/interviews", tags=["interviews"]) 