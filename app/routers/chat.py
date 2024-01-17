from typing import List

from fastapi import APIRouter
from schemas.message import Message
from ai.sql_chat_history import CustomSQLChatMessageHistory
from config.settings import settings
from ai.agent import setup_agent
from utils.session import generate_unique_session


router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)


# @router.get("")
# def get_session_list():
#     unique_session = CustomSQLChatMessageHistory(
#         session_id="None",  # Session_id is not required here
#         connection_string=settings.SQLITE_CONNECTION_STRING,
#     ).unique_session_ids()
#     pass
#
# @router.get("/{session_id}")
# def get_session_messages(session_id: str):
#     messages = CustomSQLChatMessageHistory(
#         session_id=session_id,
#         connection_string=settings.SQLITE_CONNECTION_STRING,
#     ).get_messages_by_session_id(
#         target_session_id=session_id
#     )
#     pass

@router.get("/model")
def get_model_list():
    models = settings.MODELS
    return models


@router.post("/{session_id}")
def send_message(session_id: str,data: Message):
    agent_executor = setup_agent(
        session_id=session_id,
        model=data.model
    )

    agent_executor.invoke({"input": data.message})
    return {"status": "ok"}


@router.post("")
def start_new_conversation():
    session_id = generate_unique_session()
    CustomSQLChatMessageHistory(
        session_id=session_id,
        connection_string=settings.SQLITE_CONNECTION_STRING
    ).create_conversation(session_id)

    return {"session_id": session_id}
