import langchain
from langchain.agents import AgentExecutor, OpenAIFunctionsAgent
from langchain_core.messages import SystemMessage
from langchain_core.prompts import MessagesPlaceholder

from config.settings import settings
from .tools.tools import get_tools
from .llm import get_chat_openai
from .memory import setup_memory
from .prompt import prompt

langchain.debug = settings.DEBUG


def setup_agent(session_id: str, model: str) -> AgentExecutor:
    llm = get_chat_openai(model=model)
    memory = setup_memory(session_id=session_id)
    tools = get_tools(llm=llm)

    prompt_agent = OpenAIFunctionsAgent.create_prompt(
        system_message=SystemMessage(content=prompt),
        extra_prompt_messages=[MessagesPlaceholder(variable_name="history")]
    )
    agent = OpenAIFunctionsAgent(llm=llm, tools=tools, prompt=prompt_agent)
    return AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=True,
        handle_parsing_errors=True
    )
