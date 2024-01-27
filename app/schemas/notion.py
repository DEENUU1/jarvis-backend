from pydantic import BaseModel
from datetime import datetime


class NotionSchema(BaseModel):
    page_id: str
    content: str
    embedded_at:  datetime
    updated_at: datetime


class NotionCreateSchema(BaseModel):
    page_id: str
    updated_at: datetime
    content: str


class NotionUpdateSchema(BaseModel):
    updated_at: datetime
    content: str


class NotionEmbeddUpdateSchema(BaseModel):
    embedded_at: datetime
