from typing import Optional
from enum import Enum

from pydantic import field_serializer, field_validator

from app.models.core import CoreModel, DateTimeModelMixin, UUIDModelMixin


class TaskStatus(str, Enum):
    pending = "pending"
    completed = "completed"
    cancelled = "cancelled"


class TaskBase(CoreModel):
    name: Optional[str]
    description: Optional[str]
    status: Optional[TaskStatus] = "pending"


class TaskCreate(CoreModel):
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
    name: Optional[str] = "abc"
    description: Optional[str] = "abc"
    status: Optional[TaskStatus] = "abc"
    
    model_config = {
        'json_schema_extra': {
            "examples": [
                {
                    "description": "Should be a pumpkin pie",
                    "status": "completed"
                }
            ]}
    }
    
    @field_validator('name', 'description', 'status')
    def forbid_null_value(cls, value: TaskStatus | str | None):
        if value is None:
            raise ValueError('Status cannot be None')
        return value
    
    @field_serializer('status', check_fields=False)
    def serialize_status_to_string(self, value: TaskStatus | str):
        if isinstance(value, TaskStatus):
            return value.value
        elif isinstance(value, str):
            return value


class TaskInDB(UUIDModelMixin, DateTimeModelMixin, TaskCreate, TaskBase):
    status: TaskStatus = "pending"


class TaskPublic(TaskInDB):
    pass
