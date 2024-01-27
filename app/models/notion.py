from config.database import Base
from sqlalchemy import Column, Integer, String, DateTime


class Notion(Base):
    __tablename__ = "notion"

    id = Column(Integer, primary_key=True)
    content = Column(String)
    update_at = Column(DateTime)
