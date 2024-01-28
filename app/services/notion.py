from sqlalchemy.orm import Session

from schemas.notion import NotionSchema, NotionCreateSchema, NotionUpdateSchema, NotionEmbeddUpdateSchema
from typing import Type
from config.database import NotFoundError
from models.notion import Notion


def create_notion_object(session: Session, data: NotionCreateSchema) -> NotionCreateSchema:
    notion = Notion(**data.model_dump())
    session.add(notion)
    session.commit()
    session.refresh(notion)
    return notion


def get_notion_object_by_page_id(session: Session, page_id: str) -> Type[NotionSchema]:
    notion = session.query(Notion).filter_by(page_id=page_id).first()
    if not notion:
        raise NotFoundError(f"Notion object with page_id={page_id} does not exists")
    return notion


def notion_object_exist(session: Session, page_id: str) -> bool:
    notion = session.query(Notion).filter_by(page_id=page_id).first()
    return bool(notion) if notion else False


def update_notion_content(session: Session, page_id: str, data: NotionUpdateSchema) -> Type[NotionSchema]:
    notion = get_notion_object_by_page_id(session, page_id)
    notion.content = data.content
    notion.updated_at = data.updated_at
    session.commit()
    session.refresh(notion)
    return notion


def update_notion_embedding(session: Session, page_id: str, data: NotionEmbeddUpdateSchema) -> Type[NotionSchema]:
    notion = get_notion_object_by_page_id(session, page_id)
    notion.embedding = data.embedded_at
    session.commit()
    session.refresh(notion)
    return notion
