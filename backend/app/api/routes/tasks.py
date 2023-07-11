from typing import List

from fastapi import APIRouter, Body, Depends

from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT

from app.api.dependencies.tasks import get_task_by_id_from_path
from app.api.dependencies.database import get_repository

from app.db.repositories.tasks import TaskRepository

from app.models.task import TaskCreate, TaskInDB, TaskPublic, TaskUpdate

router = APIRouter()


@router.get(
    "/",
    response_model=List[TaskPublic],
    response_description="List all tasks",
    name="task:get-all-tasks"
)
async def list_all_tasks(
        task_repo: TaskRepository = Depends(get_repository(TaskRepository))
):
    return await task_repo.list_all_tasks()


@router.get(
    "/{task_id}/",
    response_model=TaskPublic,
    response_description="Get task by id",
    name="task:get-task-by-id",
)
async def get_cleaning_by_id(
        task: TaskInDB = Depends(get_task_by_id_from_path)
) -> TaskPublic:
    return task


@router.post(
    "/",
    response_model=TaskPublic,
    response_description="Add new task",
    name="task:create-task",
    status_code=HTTP_201_CREATED,
)
async def create_new_task(
        task: TaskCreate = Body(...),
        task_repo: TaskRepository = Depends(get_repository(TaskRepository))
) -> TaskPublic:
    return await task_repo.create_task(task=task)


@router.put(
    "/{task_id}/",
    response_model=TaskPublic,
    response_description="Update task by id",
    name="task:update-task-by-id",
)
async def update_task_by_id(
        task_id: str,
        task_update: TaskUpdate = Body(...),
        task_repo: TaskRepository = Depends(get_repository(TaskRepository))
) -> TaskPublic:
    return await task_repo.update_task_by_id(task_id=task_id, task_update=task_update)


@router.delete(
    "/{task_id}/",
    response_description="Delete task by id",
    name="task:delete-task-by-id",
    status_code=HTTP_204_NO_CONTENT
)
async def delete_task(
        task_id: str,
        task_repo: TaskRepository = Depends(get_repository(TaskRepository))
):
    return await task_repo.delete_task_by_id(task_id=task_id)
