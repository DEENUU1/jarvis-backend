from langchain.memory import ConversationBufferMemory

from services.chat import CustomSQLChatMessageHistory


# from langchain_core.messages import SystemMessage
# from langchain_core.prompts import MessagesPlaceholder


# from .prompt import prompt


def setup_memory(session_id: str) -> ConversationBufferMemory:
    chat_message_history = CustomSQLChatMessageHistory(session_id=session_id)

    # agent_kwargs = {
    #     # "system_message": SystemMessage(content=prompt),
    #     "extra_prompt_messages": [MessagesPlaceholder(variable_name="history")],
    # }
    memory = ConversationBufferMemory(
        memory_key="history",
        return_messages=True,
        chat_memory=chat_message_history,
    )

    # return agent_kwargs, memory
    return memory
