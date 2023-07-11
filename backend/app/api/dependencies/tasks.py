from fastapi import Path, Depends, HTTPException
from starlette.status import HTTP_404_NOT_FOUND

from app.api.dependencies.database import get_repository
from app.db.repositories.tasks import TaskRepository
from app.models.task import TaskPublic, TaskInDB


async def get_task_by_id_from_path(
    task_id: str = Path(...),
    task_repo: TaskRepository = Depends(get_repository(TaskRepository)),
) -> TaskInDB:
    task = await task_repo.get_task_by_id(id=task_id)

    if not task:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="No task found with that id.",
        )

    return task
