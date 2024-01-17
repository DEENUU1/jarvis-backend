from typing import List, Optional, Dict

from fastapi import APIRouter

from ai.agent import setup_agent
from ai.sql_chat_history import CustomSQLChatMessageHistory
from config.settings import settings
from schemas.message import Message
from utils.session import generate_unique_session

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)


@router.get("")
def get_session_list() -> List[Optional[str]]:
    """
    Get list of unique session_id
    """

    # Session_id is not required here
    unique_session = CustomSQLChatMessageHistory(session_id="None").unique_session_ids()
    return unique_session


@router.get("/model")
def get_model_list() -> List[Optional[str]]:
    """
    Get list of available models
    """

    models = settings.MODELS
    return models


@router.post("/{session_id}")
def send_message(session_id: str, data: Message) -> Dict[str, str]:
    """
    Send message to agent
    """

    agent_executor = setup_agent(
        session_id=session_id,
        model=data.model
    )

    # agent_executor.invoke({"input": data.message})
    agent_executor.run(data.message)
    return {"status": "ok"}


@router.post("")
def start_new_conversation() -> Dict[str, str]:
    """
    Generate unique session_id and create empty Message object
    """

    session_id = generate_unique_session()
    CustomSQLChatMessageHistory(session_id=session_id).create_conversation()

    return {"session_id": session_id}


@router.get("/{session_id}")
def get_messages(session_id: str):
    """
    Get all messages for specified session_id
    """

    messages = CustomSQLChatMessageHistory(session_id=session_id).get_messages_by_session_id()
    return messages


@router.delete("/{session_id}")
def delete_conversation(session_id: str):
    """
    Delete all messages for specified session_id
    """

    CustomSQLChatMessageHistory(session_id=session_id).delete_conversation()
    return {"status": "ok"}
