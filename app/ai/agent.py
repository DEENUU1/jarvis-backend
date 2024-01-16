from langchain.agents import AgentExecutor, initialize_agent, AgentType
from langchain_community.utilities.duckduckgo_search import DuckDuckGoSearchAPIWrapper
from langchain_core.tools import Tool
from llm import get_chat_openai
from memory import setup_memory


def setup_agent(session_id: str, model: str) -> AgentExecutor:
    llm = get_chat_openai(model=model)

    duckduck_search = DuckDuckGoSearchAPIWrapper()

    tools = [
        Tool(
            name="Search",
            func=duckduck_search.run,
            description="useful for when you need to answer questions about current events. You should ask targeted questions"
        )
    ]
    agent_kwargs, memory = setup_memory(session_id=session_id)

    return initialize_agent(
        tools,
        llm,
        agent=AgentType.OPENAI_FUNCTIONS,
        verbose=False,
        agent_kwargs=agent_kwargs,
        memory=memory
    )