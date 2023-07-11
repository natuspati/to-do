from typing import Optional
from datetime import datetime
import uuid

from pydantic import BaseModel, Field, field_serializer


class CoreModel(BaseModel):
    """
    Any common logic to be shared by all models goes here
    """
    
    pass


class DateTimeModelMixin(BaseModel):
    updated: Optional[datetime] = Field(default_factory=datetime.now)
    
    @field_serializer('updated')
    def convert_datetime_to_string(self, v):
        return str(v)

class UUIDModelMixin(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, alias="_id")
    
    @field_serializer('id')
    def convert_uuid_to_string(self, v):
        return str(v)
