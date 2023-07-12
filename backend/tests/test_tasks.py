from datetime import datetime
from typing import Dict, List, Optional, Callable

import pytest

from fastapi import FastAPI, status
from async_asgi_testclient import TestClient
from fastapi.encoders import jsonable_encoder

from app.models.task import TaskPublic

pytestmark = pytest.mark.asyncio


class TestTaskRoutes:
    """
    Check each task route to ensure none return 404s
    """
    
    async def test_routes_exist(self, app: FastAPI, client: TestClient, test_task: TaskPublic) -> None:
        res = await client.post(app.url_path_for("task:create-task"), json={})
        assert res.status_code != status.HTTP_404_NOT_FOUND
        res = await client.get(app.url_path_for("task:get-task-by-id", task_id=test_task.id))
        assert res.status_code != status.HTTP_404_NOT_FOUND
        res = await client.get(app.url_path_for("task:get-all-tasks"))
        assert res.status_code != status.HTTP_404_NOT_FOUND
        res = await client.put(app.url_path_for("task:get-task-by-id", task_id=test_task.id))
        assert res.status_code != status.HTTP_404_NOT_FOUND
        res = await client.delete(app.url_path_for("task:delete-task-by-id", task_id=test_task.id))
        assert res.status_code != status.HTTP_404_NOT_FOUND


class TestTaskCreate:
    async def test_valid_input_creates_task(
            self, app: FastAPI, client: TestClient, new_task: dict
    ) -> None:
        res = await client.post(
            app.url_path_for("task:create-task"), json=new_task
        )
        assert res.status_code == status.HTTP_201_CREATED
        
        created_task = TaskPublic(**res.json())
        assert created_task.name == new_task["name"]
        assert created_task.description == new_task["description"]
    
    @pytest.mark.parametrize(
        "invalid_payload, status_code",
        (
                (None, 422),
                ({}, 422),
                ({"name": "test"}, 422),
                ({"description": "test"}, 422),
                ({"task": {"name": "test", "description": "test"}}, 422),
        ),
    )
    async def test_invalid_input_raises_error(
            self,
            app: FastAPI,
            client: TestClient,
            invalid_payload: Dict[str, str],
            status_code: int,
    ) -> None:
        res = await client.post(
            app.url_path_for("task:create-task"), json=invalid_payload
        )
        assert res.status_code == status_code


class TestGetTask:
    async def test_get_task_by_id(
            self, app: FastAPI, client: TestClient, test_task: TaskPublic
    ) -> None:
        res = await client.get(
            app.url_path_for("task:get-task-by-id", task_id=test_task.id)
        )
        assert res.status_code == status.HTTP_200_OK
        
        task = TaskPublic(**res.json()).model_dump()
        assert task == test_task.model_dump()
    
    @pytest.mark.parametrize(
        "id, status_code", ((50000, 404), (-1, 404), (None, 404)),
    )
    async def test_wrong_id_returns_error(
            self, app: FastAPI, client: TestClient, id: int, status_code: int
    ) -> None:
        res = await client.get(app.url_path_for("task:get-task-by-id", task_id=id))
        assert res.status_code == status_code
    
    async def test_get_all_tasks(
            self,
            app: FastAPI,
            client: TestClient,
            test_list_of_tasks: List[TaskPublic],
    ) -> None:
        res = await client.get(app.url_path_for("task:get-all-tasks"))
        assert res.status_code == status.HTTP_200_OK
        
        assert (res.json(), list)
        assert len(res.json()) > 0
        
        # Check fixture task ids are present among fetched tasks
        fetched_task_ids = [t["_id"] for t in res.json()]
        assert all(str(t.id) in fetched_task_ids for t in test_list_of_tasks)


class TestUpdateTask:
    @pytest.mark.parametrize(
        "attrs_to_change, values",
        (
                (["name"], ["Updated name"]),
                (["description"], ["Updated description"]),
                (["status"], ["completed"]),
                (["name", "description"], ["Update name and description", "Update description and name"]),
                (["description", "status"], ["Updated description and status", "cancelled"]),
        ),
    )
    async def test_update_task_with_valid_input(
            self,
            app: FastAPI,
            client: TestClient,
            test_task: TaskPublic,
            attrs_to_change: List[str],
            values: List[str],
    ) -> None:
        task_update = {attrs_to_change[i]: values[i] for i in range(len(attrs_to_change))}
        res = await client.put(
            app.url_path_for("task:update-task-by-id", task_id=test_task.id), json=task_update
        )
        assert res.status_code == status.HTTP_200_OK
        
        # make sure the updated task is the same
        updated_task = TaskPublic.model_validate(res.json())
        assert updated_task.id == test_task.id
        
        # make sure that any updated attribute has changed to the correct value
        for i in range(len(attrs_to_change)):
            assert getattr(updated_task, attrs_to_change[i]) != getattr(test_task, attrs_to_change[i])
            assert getattr(updated_task, attrs_to_change[i]) == values[i]
        
        # make sure that no other attributes' values have changed
        for attr, value in updated_task.model_dump().items():
            if attr not in attrs_to_change and attr != "updated":
                if attr == "id":
                    assert str(getattr(test_task, attr)) == value
                else:
                    assert getattr(test_task, attr) == value
    
    @pytest.mark.parametrize(
        "payload, status_code",
        (
                ({}, 304),
                (jsonable_encoder({"updated": datetime.now()}), 304),
                ({"name": 1}, 422),
                (None, 422),
                ({"status": "invalid status"}, 422),
                ({"status": None}, 422),
                ({"name": None, "description": None}, 422),
        ),
    )
    async def test_update_task_with_invalid_input_throws_error(
            self,
            app: FastAPI,
            client: TestClient,
            test_task: TaskPublic,
            payload: Dict[str, Optional[str | int | None]],
            status_code: int
    ) -> None:
        res = await client.put(
            app.url_path_for("task:update-task-by-id", task_id=test_task.id), json=payload
        )
        assert res.status_code == status_code



class TestDeleteTask:
    async def test_can_delete_task_successfully(
            self, app: FastAPI, client: TestClient, test_task: TaskPublic
    ) -> None:
        res = await client.delete(
            app.url_path_for("task:delete-task-by-id", task_id=test_task.id)
        )
        assert res.status_code == status.HTTP_204_NO_CONTENT

    @pytest.mark.parametrize(
        "id, status_code", ((1, 404), ('1', 404), (None, 404)),
    )
    async def test_wrong_id_throws_error(
            self,
            app: FastAPI,
            client: TestClient,
            id: str,
            status_code: int
    ) -> None:
        res = await client.delete(app.url_path_for("task:delete-task-by-id", task_id=id))
        assert res.status_code == status_code
