from langchain.agents import AgentExecutor, OpenAIFunctionsAgent  # initialize_agent, AgentType,
from langchain_community.utilities.duckduckgo_search import DuckDuckGoSearchAPIWrapper
from langchain_core.messages import SystemMessage
from langchain_core.prompts import MessagesPlaceholder
from langchain_core.tools import Tool

from .llm import get_chat_openai
from .memory import setup_memory
from .prompt import prompt
from langchain.chains import RetrievalQA
from .vector import get_pinecone
import langchain

langchain.debug = True


def setup_agent(session_id: str, model: str) -> AgentExecutor:
    llm = get_chat_openai(model=model)
    duckduck_search = DuckDuckGoSearchAPIWrapper()
    # _, memory = setup_memory(session_id=session_id)
    memory = setup_memory(session_id=session_id)

    personal_data = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=get_pinecone().as_retriever(),
    )

    tools = [
        Tool(
            name="Search",
            func=duckduck_search.run,
            description="Useful for when you need to answer questions about current events. You should ask targeted questions"
        ),
        Tool(
            name="User-private-data",
            func=personal_data.run,
            description="Useful when you need to answer questions about user's personal data"
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
        verbose=True,
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
