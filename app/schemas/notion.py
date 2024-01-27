from pydantic import BaseModel
from datetime import datetime


class NotionSchema(BaseModel):
    page_id: str
    content: str
    embedded_at:  datetime
    updated_at: datetime
