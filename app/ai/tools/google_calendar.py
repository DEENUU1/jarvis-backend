from typing import Union, Dict, Tuple
from langchain_core.tools import BaseTool
from ai.integration.google_calendar import Calendar


class GoogleCalendarListEventTool(BaseTool):
    name = "google_calendar_list_event_tool"
    description = "Useful for when you need to answer questions about events from Google calendar"

    def _to_args_and_kwargs(self, tool_input: Union[str, Dict]) -> Tuple[Tuple, Dict]:
        return (), {}

    def _run(self) -> str:
        calendar = Calendar()
        return calendar.get_all_events()

    async def _arun(self) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")
