from fastapi import APIRouter, Request
from app.modules.health.service import ping

router = APIRouter(prefix="/health", tags=["Health"])

@router.get("/ping", summary="Test API is alive")
async def ping_fastAPI():
    return await ping()