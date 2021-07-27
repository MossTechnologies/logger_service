from fastapi import APIRouter

from src.apps.logging_.routers import log_router


router = APIRouter()
router.include_router(
	log_router, prefix='/logging'
)
