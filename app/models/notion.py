from config.database import Base
from sqlalchemy import Column, Integer, String, DateTime


class Notion(Base):
    __tablename__ = "notion"

    id = Column(Integer, primary_key=True)
    content = Column(String)
    embedded_at = Column(DateTime)
    updated_at = Column(DateTime)
