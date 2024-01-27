from sqlalchemy.orm import Session

from schemas.notion import NotionSchema
from typing import Type
from config.database import NotFoundError


def create_notion_object(session: Session, data: NotionSchema) -> NotionSchema:
    notion = NotionSchema(**data.dict())
    session.add(notion)
    session.commit()
    session.refresh(notion)
    return notion


def get_notion_object_by_page_id(session: Session, page_id: str) -> Type[NotionSchema]:
    notion = session.query(NotionSchema).filter_by(page_id=page_id).first()
    if not notion:
        raise NotFoundError(f"Notion object with page_id={page_id} does not exists")
    return notion
