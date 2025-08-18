#   Goal:
# Create an API that exposes a calendar.
# Features:
# - Query it for todays date and time
# - CRUD operations of events
# - Send out relative times to events (e.g. 3 days, 20 hours, 54 minutes from now)
# - Allow for listing of events

from uuid import UUID
from datetime import date, time, datetime
from typing import Annotated

from fastapi import FastAPI
from pydantic import BaseModel

import database as db

class Event(BaseModel):
    id: UUID | None = None
    date: date
    time: time
    name: str
    description: str | None = None
    location: str | None = None

app = FastAPI()
app_db = db.DataBase()

db.create_test_events(app_db)
def fill_db_event(new_event: Event) -> db.Event:
    db_event = db.Event(new_event.name)
    db_event.date = new_event.date
    db_event.time = new_event.time
    db_event.description = new_event.description
    db_event.location = new_event.location
    return db_event

@app.get("/")
async def get_main():
    return {"message": "Welcome to the calendar! The time is currently: " + str(datetime.now())}

@app.get("/today")
async def get_today():
    return {"date_time": str(datetime.now()), "events_today": app_db.dates[date.today()]}

@app.get("/events")
async def get_events():
    return {"events": app_db.events}

@app.get("/events/ids")
async def get_event_ids():
    return {"ids": [elem for elem in app_db.events.keys()]}

@app.post("/events/new")
async def add_event(new_event: Event):
    db_event = fill_db_event(new_event)
    id = app_db.add_event(db_event)
    return {"event": app_db.events[id]}

@app.delete("/events/remove/{id}")
async def remove_event(id: UUID, should_return: bool = False):
    event = app_db.delete_event(id)
    if not should_return:
        return {}
    return {"event": event}

@app.put("/events/update/{id}")
async def update_event(id: UUID, new_event: Event):
    db_event = fill_db_event(new_event)
    db_event.id = id
    app_db.update_event(db_event)
    return {"event": app_db.events[id]}

@app.get("/events/id/{id}")
async def get_event(id: UUID):
    return {"event": app_db.events[id]}

@app.get("/events/today")
async def get_events_today():
    return {"events": app_db.dates[date.today()]}

@app.get("/events/{year}/{month}/{day}")
async def get_events_date(year: int, month: int, day: int, id_only: bool):
    if id_only:
        return {"events": [elem.id for elem in app_db.dates[date(year, month, day)]]}
    return {"events": app_db.dates[date(year, month, day)]}