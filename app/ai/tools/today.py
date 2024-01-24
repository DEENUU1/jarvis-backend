import datetime
from typing import Union, Dict, Tuple
from langchain_core.tools import BaseTool


def get_current_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class CurrentTimeTool(BaseTool):
    name = "current_time_tool"
    description = "Useful for when you need to answer questions about current date and time"

    def _to_args_and_kwargs(self, tool_input: Union[str, Dict]) -> Tuple[Tuple, Dict]:
        return (), {}

    def _run(self) -> str:
        return get_current_time()

    async def _arun(self) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")
