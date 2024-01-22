from pydantic import BaseModel


class Message(BaseModel):
    message: str
    model: str = "gpt-3.5-turbo-16k-0613"
