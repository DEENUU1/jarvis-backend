from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import MessagesPlaceholder

from .sql_chat_history import CustomSQLChatMessageHistory
from config.settings import settings


def setup_memory(session_id: str):
    chat_message_history = CustomSQLChatMessageHistory(session_id=session_id)

    agent_kwargs = {
        "extra_prompt_messages": [MessagesPlaceholder(variable_name="history")],
    }
    memory = ConversationBufferMemory(
        memory_key="history",
        return_messages=True,
        chat_memory=chat_message_history,
    )

    return agent_kwargs, memory
