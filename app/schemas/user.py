from pydantic import BaseModel
from config.settings import settings


class User(BaseModel):
    first_name: str = settings.FIRST_NAME
    last_name: str = settings.LAST_NAME
    location: str = settings.LOCATION


