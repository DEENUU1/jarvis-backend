from config.database import Base
from sqlalchemy import Column, Integer, String, DateTime


class Notion(Base):
    __tablename__ = "notion"

    page_id = Column(String, primary_key=True)
    content = Column(String, nullable=True)
    embedded_at = Column(DateTime, nullable=True, default=None)
    updated_at = Column(DateTime, nullable=True, default=None)
