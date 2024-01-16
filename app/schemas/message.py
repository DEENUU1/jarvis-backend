from pydantic import BaseModel


class Message(BaseModel):
    message: str
    session_id: str
    model: str