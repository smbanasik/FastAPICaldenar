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

@app.get("/")
async def get_main():
    message = "Welcome to the calendar! The time is currently: " + str(datetime.now())
    return {"message": message}

@app.get("/today")
async def get_today():
    return {"date_time": str(datetime.now())}

@app.get("/events")
async def get_events():
    return app_db.events

@app.post("/events/new")
async def add_event(new_event: Event):

    db_event = db.Event(new_event.name)
    db_event.date = new_event.date
    db_event.time = new_event.time
    db_event.description = new_event.description
    db_event.location = new_event.location
    id = app_db.add_event(db_event)
    return app_db.events[id]

@app.get("/events/today")
async def get_events_today(max_events: int | None = None):
    return app_db.dates[date.today()]