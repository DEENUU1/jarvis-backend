from typing import List, Optional, Dict

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from ai.agent import setup_agent
from config.settings import settings
from schemas.message import Message
from services.chat import CustomSQLChatMessageHistory
from utils.session import generate_unique_session

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)


@router.get(
    "/",
    response_class=JSONResponse,
    status_code=status.HTTP_200_OK,
    summary="Get list of unique session_id"
)
def get_session_list() -> JSONResponse:
    """
    Get list of unique session_id
    """

    # Session_id is not required here
    unique_session = CustomSQLChatMessageHistory(session_id="None").unique_session_ids()
    return JSONResponse(content={"session_ids": unique_session})


@router.get(
    "/model",
    response_model=List[str],
    status_code=status.HTTP_200_OK,
    summary="Get list of available models"
)
def get_model_list() -> List[Optional[str]]:
    """
    Get list of available models
    """

    models = settings.MODELS
    return models


@router.post(
    "/{session_id}",
    response_model=Dict[str, str],
    status_code=status.HTTP_201_CREATED,
    summary="Send message to agent"
)
def send_message(session_id: str, data: Message) -> Dict[str, str]:
    """
    Send message to agent
    """
    try:
        agent_executor = setup_agent(
            session_id=session_id,
            model=data.model
        )
        agent_executor.run(data.message)
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.post(
    "/",
    response_model=Dict[str, str],
    status_code=status.HTTP_201_CREATED,
    summary="Start new conversation"
)
def start_new_conversation() -> Dict[str, str]:
    """
    Generate unique session_id and create empty Message object
    """

    session_id = generate_unique_session()
    CustomSQLChatMessageHistory(session_id=session_id).create_conversation()

    return {"session_id": session_id}


@router.get(
    "/{session_id}",
    status_code=status.HTTP_200_OK,
    summary="Get all messages for specified conversation"
)
def get_messages(session_id: str):
    """
    Get all messages for specified session_id
    """

    messages = CustomSQLChatMessageHistory(session_id=session_id).get_messages_by_session_id()
    return messages


@router.delete(
    "/{session_id}",
    response_model=Dict[str, str],
    status_code=status.HTTP_200_OK,
    summary="Delete specified conversation including all messages"
)
def delete_conversation(session_id: str) -> Dict[str, str]:
    """
    Delete all messages for specified session_id
    """

    CustomSQLChatMessageHistory(session_id=session_id).delete_conversation()
    return {"status": "ok"}
