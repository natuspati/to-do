from typing import List

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from starlette import status

from app.db.repositories.base import BaseRepository
from app.models.task import TaskCreate, TaskPublic, TaskInDB, TaskModel, TaskUpdate


class TaskRepository(BaseRepository):
    """"
    All database actions associated with the Task resource
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.collection = self.db.get_collection("tasks")
    
    async def list_all_tasks(self) -> List[TaskPublic]:
        task_records = await self.collection.find().to_list(10)
        
        return [TaskPublic.model_validate(t) for t in task_records]
    
    async def create_task(self, *, task: TaskCreate) -> TaskPublic:
        encoded_task = jsonable_encoder(task)
        new_task = await self.collection.insert_one(encoded_task)
        created_task = await self.collection.find_one(
            {"_id": new_task.inserted_id}
        )
        
        return TaskPublic.model_validate(created_task)
    
    async def get_task_by_id(self, *, id: str, ) -> TaskPublic:
        if (task := await self.collection.find_one({"_id": id})) is not None:
            return TaskPublic.model_validate(task)
    
    async def update_task_by_id(self, task_id: str, task_update: TaskUpdate) -> TaskPublic:
        task_items = {}
        for k, v in task_update.model_dump().items():
            if v is not None:
                task_items[k] = v
        
        await self.collection.update_one(
            {"_id": task_id}, {"$set": task_items}
        )
        
        if (
                updated_task := await self.collection.find_one({"_id": task_id})
        ) is None:
            raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
        
        return TaskPublic.model_validate(updated_task)
    
    async def delete_task_by_id(self, task_id: str):
        delete_result = await self.collection.delete_one({"_id": task_id})
        
        if delete_result.deleted_count != 1:
            raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
        
        return None
