import os
import warnings
from typing import List, Callable

import pytest
import pytest_asyncio
from pymongo import MongoClient

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from async_asgi_testclient import TestClient
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.config import DATABASE_URL, DATABASE_NAME
from app.models.task import TaskCreate, TaskPublic, TaskUpdate
from app.db.repositories.tasks import TaskRepository


@pytest.fixture(scope="session")
def prepare_test_env() -> None:
    # Create synchronous Mongodb and set testing to True
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    os.environ["TESTING"] = "1"
    mongo_client = MongoClient(DATABASE_URL)
    
    yield None
    
    # Drop test database
    mongo_client.drop_database(f"{DATABASE_NAME}_test")
    database_list = mongo_client.list_database_names()
    assert len(database_list) == 3


@pytest_asyncio.fixture
def app(prepare_test_env: None) -> FastAPI:
    from app.api.server import get_application
    return get_application()


@pytest_asyncio.fixture
def db(app: FastAPI) -> AsyncIOMotorDatabase:
    return app.database


@pytest_asyncio.fixture
async def client(app: FastAPI) -> TestClient:
    async with TestClient(app, headers={"Content-Type": "application/json"}) as client:
        yield client


@pytest_asyncio.fixture
def new_task() -> dict:
    created_task = TaskCreate(
        name="Test task", description="Test description",
    )
    return jsonable_encoder(created_task)


@pytest_asyncio.fixture
def new_task_factory():
    def _new_task(i: int):
        created_task = TaskCreate(
            name=f"Test task {i}", description=f"Test description {i}",
        )
        return jsonable_encoder(created_task)
    
    return _new_task


@pytest_asyncio.fixture
async def test_task(db: AsyncIOMotorDatabase, new_task: dict) -> TaskPublic:
    task_repo = TaskRepository(db)
    task = TaskCreate.model_validate(new_task)
    return await task_repo.create_task(task=task)


@pytest_asyncio.fixture
def test_task_factory(db: AsyncIOMotorDatabase, new_task: dict) -> Callable:
    async def _test_task(status: str) -> TaskPublic:
        task_repo = TaskRepository(db)
        
        new_task["name"] = f"{status} task"
        created_task = await task_repo.create_task(task=TaskCreate.model_validate(new_task))
        updated_task = await task_repo.update_task_by_id(
            task_id=str(created_task.id),
            task=created_task,
            task_update=TaskUpdate.model_validate({"status": status})
        )
        return updated_task
    
    return _test_task


@pytest_asyncio.fixture
async def test_list_of_tasks(db: AsyncIOMotorDatabase, new_task_factory: Callable) -> List[TaskPublic]:
    task_repo = TaskRepository(db)
    new_tasks = [
        await task_repo.create_task(
            task=TaskCreate.model_validate(new_task_factory(i=i))
        )
        for i in range(5)
    ]
    
    return new_tasks
