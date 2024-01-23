from gcsa.google_calendar import GoogleCalendar
from config.settings import settings
from typing import Optional, Dict


class Calendar:

    def __init__(self) -> None:
        self._calendar = GoogleCalendar(
            settings.GOOGLE_CALENDAR_EMAIL,
            credentials_path="credentials.json",
            authentication_flow_port=8081,
            authentication_flow_host="0.0.0.0"
        )
        self._calendar_ids = settings.GOOGLE_CALENDARS
        self.debug: bool = settings.GOOGLE_CALENDAR_DEBUG

    @staticmethod
    def _get_calendars() -> Dict[str, str]:
        return settings.GOOGLE_CALENDARS

    def get_all_events(self) -> Optional[str]:
        events = ""
        for calendar_id in self._calendar_ids.values():
            if self.debug:
                print(f"Getting events from calendar {calendar_id}")

            calendar_event = self._calendar.get_events(calendar_id=calendar_id)
            for event in calendar_event:
                if self.debug:
                    print(f"Event: {event.summary}")

                event_summary = event.summary
                event_start = event.start
                event_end = event.end
                event_description = event.description
                event_location = event.location

                event_str = "Event: "
                if event_summary:
                    event_str += f"Title: {event_summary} "
                if event_start:
                    event_str += f"Start: {event_start} "
                if event_end:
                    event_str += f"End: {event_end} "
                if event_description:
                    event_str += f"Description: {event_description} "
                if event_location:
                    event_str += f"Location: {event_location} "

                events += event_str + "\n"

        return events

    def create_event(self) -> None:
        pass

    def search_event(self) -> None:
        pass

    def delete_event(self) -> None:
        pass

    def get_event(self) -> None:
        pass

    def update_event(self) -> None:
        pass
