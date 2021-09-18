from fastapi import APIRouter
from src.apps.logging_.endpoints import logger


log_router = APIRouter()
log_router.include_router(
	logger.router
)
