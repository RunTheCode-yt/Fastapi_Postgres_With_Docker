import uuid
from typing import Optional
from pydantic import ConfigDict, BaseModel


class ItemCreate(BaseModel):
    title: str
    description: Optional[str] = None


class ItemResponse(BaseModel):
    id: uuid.UUID
    title: str
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)