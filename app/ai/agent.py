from langchain.agents import AgentExecutor, OpenAIFunctionsAgent
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
from config.settings import settings
# from langchain_community.utilities.openweathermap import OpenWeatherMapAPIWrapper
from langchain.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

langchain.debug = True


def setup_agent(session_id: str, model: str) -> AgentExecutor:
    llm = get_chat_openai(model=model)
    duckduck_search = DuckDuckGoSearchAPIWrapper()
    # _, memory = setup_memory(session_id=session_id)
    memory = setup_memory(session_id=session_id)

    personal_data = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=get_pinecone(settings.PINECONE_PRIVATE_INDEX).as_retriever(
            search_type="similarity",
            search_kwargs={"k": 3}
        ),
    )

    learning_data = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=get_pinecone(settings.PINECONE_LEARNING_INDEX).as_retriever(
            search_type="similarity",
            search_kwargs={"k": 3}
        )
    )

    work_data = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=get_pinecone(settings.PINECONE_WORK_INDEX).as_retriever(
            search_type="similarity",
            search_kwargs={"k": 3}
        )
    )

    it_data = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=get_pinecone(settings.PINECONE_IT_INDEX).as_retriever(
            search_type="similarity",
            search_kwargs={"k": 3}
        )
    )

    # weather = OpenWeatherMapAPIWrapper(openweathermap_api_key=settings.OPENWEATHERAPP_API_KEY)
    wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
    tools = [
        Tool(
            name="Wikipedia",
            func=wikipedia.run,
            description="Useful when you need to answer questions about current events. You should ask targeted questions"
        ),
        # Tool(
        #     name="Weather",
        #     func=weather.run,
        #     description="Useful for when you need to answer questions about current weather"
        # ),
        Tool(
            name="Search",
            func=duckduck_search.run,
            description="Useful for when you need to answer questions about current events. You should ask targeted questions"
        ),
        Tool(
            name="User-private-data",
            func=personal_data.run,
            description="Useful when you need to answer questions about user's personal data"
        ),
        Tool(
            name="User-work-data",
            func=work_data.run,
            description="Useful when you need to answer about user's work like freelancing projects"
        ),
        Tool(
            name="User-learning",
            func=learning_data.run,
            description="Useful when you need to answer about user's studies and learning resources like read articles, videos etc"
        ),
        Tool(
            name="User-it",
            func=it_data.run,
            description="Useful when you need to answer about user's IT projects, computer science and other related fields "
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
