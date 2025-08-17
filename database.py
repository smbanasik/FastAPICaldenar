from datetime import datetime, date, time
from uuid import UUID, uuid4
from typing import Dict, List
from collections import defaultdict

# Event class
class Event:
    def __init__(self, name):
        self.date: date
        self.time: time | None = None
        self.id: UUID
        self.name: str = ""
        self.description: str | None = None
        self.location: str | None = None


# Store events
class DataBase:
    def __init__(self):
        self.events: Dict[UUID, Event] = {}
        self.dates: Dict[date, List[Event]] = defaultdict(list)

    def get_event(self, id: UUID) -> Event:
        return self.events[id]

    def get_events(self, date: date) -> List[Event]:
        return self.dates[date]

    def add_event(self, new_event: Event):
        id = uuid4()
        new_event.id = id
        self.events[id] = new_event
        self.dates[new_event.date].append(new_event)
        return id

    def delete_event(self, id: UUID):
        event_date = self.events[id].date
        new_events = [elem for elem in self.dates[event_date] if elem.id != id]
        self.dates[event_date] = new_events
        del self.events[id]

    # TODO: check if date has changed and if so move it from one date time to another
    def update_event(self, new_event: Event):
        self.events[new_event.id] = new_event