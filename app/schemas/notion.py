from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class NotionSchema(BaseModel):
    page_id: str
    content: Optional[str] = None
    embedded_at:  Optional[datetime] = None
    updated_at: datetime


class NotionCreateSchema(BaseModel):
    page_id: str
    updated_at: datetime
    content: Optional[str] = None


class NotionUpdateSchema(BaseModel):
    updated_at: datetime
    content: Optional[str] = None


class NotionEmbeddUpdateSchema(BaseModel):
    embedded_at: datetime
