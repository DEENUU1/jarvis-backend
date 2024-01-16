from fastapi import APIRouter
from services.sql_chat_history import CustomSQLChatMessageHistory
from config.settings import settings

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)


@router.get("", tags=["session_list"])
def get_session_list(session_id: str = None):
    unique_session = CustomSQLChatMessageHistory(
        session_id=session_id,
        connection_string=settings.SQLITE_CONNECTION_STRING,
    ).unique_session_ids()
    print(unique_session)
