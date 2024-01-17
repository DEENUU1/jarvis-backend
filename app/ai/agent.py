from langchain.agents import AgentExecutor, OpenAIFunctionsAgent  # initialize_agent, AgentType,
from langchain_community.utilities.duckduckgo_search import DuckDuckGoSearchAPIWrapper
from langchain_core.messages import SystemMessage
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.tools import Tool

from .llm import get_chat_openai
from .memory import setup_memory
from .prompt import prompt


def setup_agent(session_id: str, model: str):
    llm = get_chat_openai(model=model)
    duckduck_search = DuckDuckGoSearchAPIWrapper()
    # _, memory = setup_memory(session_id=session_id)
    memory = setup_memory(session_id=session_id)

    tools = [
        Tool(
            name="Search",
            func=duckduck_search.run,
            description="useful for when you need to answer questions about current events. You should ask targeted questions"
        )
    ]

    prompt_agent = OpenAIFunctionsAgent.create_prompt(
        system_message=SystemMessage(
            content=(
                prompt
            )
        ),
        extra_prompt_messages=[MessagesPlaceholder(variable_name="history")]
    )
    agent = OpenAIFunctionsAgent(llm=llm, tools=tools, prompt=prompt_agent)
    return AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=False,
        handle_parsing_errors=True
    )

    # return initialize_agent(
    #     tools,
    #     llm,
    #     agent=AgentType.OPENAI_FUNCTIONS,
    #     verbose=False,
    #     agent_kwargs=agent_kwargs,
    #     memory=memory
    # )
