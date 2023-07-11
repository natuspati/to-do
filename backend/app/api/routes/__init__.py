from fastapi import APIRouter
from app.api.routes.tasks import router as task_router

router = APIRouter()
router.include_router(task_router, prefix="/tasks", tags=["tasks"])
