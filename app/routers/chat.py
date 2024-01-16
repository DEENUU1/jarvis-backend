from fastapi import APIRouter
from ai.sql_chat_history import CustomSQLChatMessageHistory
from config.settings import settings

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)


@router.get("", tags=["session_list"])
def get_session_list():
    unique_session = CustomSQLChatMessageHistory(
        session_id="None",  # Session_id is not required here
        connection_string=settings.SQLITE_CONNECTION_STRING,
    ).unique_session_ids()
    print(unique_session)


@router.get("/{session_id}", tags=["session_messages"])
def get_session_messages(session_id: str):
    messages = CustomSQLChatMessageHistory(
        session_id=session_id,
        connection_string=settings.SQLITE_CONNECTION_STRING,
    ).get_messages_by_session_id(
        target_session_id=session_id
    )

    print(messages)
