from gcsa.google_calendar import GoogleCalendar
from config.settings import settings
from typing import List, Optional, Dict
from gcsa.event import Event


class Calendar:

    def __init__(self) -> None:
        self._calendar = GoogleCalendar(settings.GOOGLE_CALENDAR_EMAIL)
        self._calendar_ids = settings.GOOGLE_CALENDARS
        self.debug: bool = settings.GOOGLE_CALENDAR_DEBUG

    @staticmethod
    def _get_calendars() -> Dict[str, str]:
        return settings.GOOGLE_CALENDARS

    def get_all_events(self) -> List[Optional[Event]]:
        events = []
        for calendar_id in self._calendar_ids.values():
            if self.debug:
                print(f"Getting events from calendar {calendar_id}")

            calendar_event = self._calendar.get_events(calendar_id=calendar_id)
            for event in calendar_event:
                if self.debug:
                    print(f"Event: {event.summary}")

                events.append(event)

        return events
