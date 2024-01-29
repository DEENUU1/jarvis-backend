from datetime import timezone

from ai.vector import save_to_pinecone
from ai.vector import split_files
from config.settings import settings
from integration.notion import notion
from schemas.notion import NotionCreateSchema, NotionUpdateSchema
from services import notion as ns
from services.chat import get_all_conversations


def chat_history_embedding_task():
    try:
        conversations = get_all_conversations()
        for conversation in conversations:
            chunks = split_files(data=conversation)
            save_to_pinecone(chunks)
    except Exception as e:
        print(e)
        raise e


def fetch_notion_task(db):
    try:
        for dbs in settings.NOTION_DATABASES:
            parsed_pages = notion(dbs=dbs)
            for page in parsed_pages:
                if page:
                    if ns.notion_object_exist(db, page_id=page.page_id):
                        existing_object = ns.get_notion_object_by_page_id(db, page_id=page.page_id)
                        existing_object_updated_at = existing_object.updated_at.replace(tzinfo=timezone.utc)

                        if existing_object_updated_at < page.updated_at:
                            ns.update_notion_content(
                                session=db,
                                page_id=page.page_id,
                                data=NotionUpdateSchema(
                                    updated_at=page.updated_at,
                                    content=page.content,
                                )
                            )
                        else:
                            continue
                    else:
                        ns.create_notion_object(
                            db,
                            NotionCreateSchema(
                                page_id=page.page_id,
                                updated_at=page.updated_at,
                                content=page.content,
                            )
                        )
    except Exception as e:
        print(e)
        raise e


def notion_embedding_task(db):
    try:
        notion_objects = ns.get_all_notion_objects(db)
        for notion_object in notion_objects:
            if notion_object.embedded_at is None or notion_object.embedded_at < notion_object.updated_at:
                chunks = split_files(data=notion_object.content)
                save_to_pinecone(chunks)
                ns.update_notion_embedding(
                    session=db,
                    page_id=notion_object.page_id
                )
            else:
                continue
    except Exception as e:
        print(e)
        raise e
