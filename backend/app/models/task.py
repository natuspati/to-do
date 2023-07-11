from typing import Optional
from enum import Enum

from pydantic import BaseModel, Field, field_serializer

from app.models.core import CoreModel, DateTimeModelMixin, UUIDModelMixin


class TaskStatus(str, Enum):
    pending = "pending"
    completed = "completed"
    cancelled = "cancelled"


class TaskBase(CoreModel):
    name: Optional[str]
    description: Optional[str]
    status: Optional[TaskStatus] = "pending"


class TaskCreate(UUIDModelMixin, DateTimeModelMixin, TaskBase):
    name: str
    description: str
    
    model_config = {
        'json_schema_extra': {
            "examples": [
                {
                    "name": "Cook a pie",
                    "description": "Should be an apple pie"
                }
            ]}
    }


class TaskUpdate(TaskBase):
    name: Optional[str] = ''
    descriptions: Optional[str] = ''
    status: Optional[TaskStatus] = 'pending'

    model_config = {
        'json_schema_extra': {
            "examples": [
                {
                    "description": "Should be an pumpkin pie",
                    "status": "completed"
                }
            ]}
    }
    
    @field_serializer('status', check_fields=False)
    def convert_status_to_string(self, value: TaskStatus | str):
        if isinstance(value, TaskStatus):
            return value.value
        elif isinstance(value, str):
            return value


class TaskInDB(TaskCreate):
    status: TaskStatus = "pending"


class TaskPublic(TaskInDB):
    pass


class TaskModel(UUIDModelMixin, DateTimeModelMixin, TaskBase):
    name: str
    description: str
    status: Optional[TaskStatus] = "pending"
