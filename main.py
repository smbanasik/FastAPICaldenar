#   Goal:
# Create an API that exposes a calendar.
# Features:
# - Query it for todays date and time
# - CRUD operations of events
# - Send out relative times to events (e.g. 3 days, 20 hours, 54 minutes from now)
# - Allow for listing of events

from contextlib import asynccontextmanager
from uuid import UUID
from datetime import date, time, datetime
from typing import Tuple, Dict, List, Iterable
import aiosqlite

from fastapi import FastAPI, status
from pydantic import BaseModel

from . import db_new as mydb

class Event(BaseModel):
    id: UUID | None = None
    date: date
    time: time
    name: str
    description: str | None = None
    location: str | None = None

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await mydb.table_drop(db, "events_prod")

        await mydb.table_create(db, "events_prod", 
        ["id TEXT PRIMARY KEY", "year INTEGER NOT NULL", "month INTEGER NOT NULL",
        "day INTEGER NOT NULL", "hour INTEGER", "minutes INTEGER",
        "name TEXT NOT NULL", "location TEXT", "description TEXT"])

        await mydb.event_insert(db, date.today(), "Test") # Test insert

@asynccontextmanager
async def lifespan(app: FastAPI):

    await init_db()
    yield
    # Closing code as needed

app = FastAPI(lifespan=lifespan)
DB_NAME: str = "calendar.db"

def convert_tuple(event: aiosqlite.Row) -> Dict[str, str]:
    out = {}
    out["id"] = event[0]
    out["date"] = date(event[1], event[2], event[3])
    if event[4] is not None:
        out["time"] = time(event[4], event[5])
    out["name"] = event[6]
    if event[7] is not None:
        out["location"] = event[7]
    if event[8] is not None:
        out["description"] = event[8]
    return out

def convert_tuples(events: Iterable[aiosqlite.Row]) -> List[Dict[str, str]]:
    out = [convert_tuple(event) for event in events]
    return out

@app.get("/")
async def get_main():
    return {"message": "Welcome to the calendar! The time is currently: " + str(datetime.now())}

@app.get("/today")
async def get_today():

    today: date = date.today()

    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute('''SELECT * FROM events_prod
        WHERE year = (?) AND month = (?) AND day = (?)
        ''', [today.year, today.month, today.day])
        
        rows = await cursor.fetchall()
        await cursor.close()

    return {"date_time": str(datetime.now()), "events": convert_tuples(rows)}

@app.get("/events")
async def get_events():
    async with aiosqlite.connect(DB_NAME) as db:
         cursor = await db.execute("SELECT * FROM events_prod")
         rows = await cursor.fetchall()
         await cursor.close()

    return {"events": convert_tuples(rows)}

@app.get("/events/ids")
async def get_event_ids():

    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute("SELECT id FROM events_prod")
        rows = await cursor.fetchall()
        await cursor.close()

    return {"ids": rows}


@app.post("/events/new", status_code=status.HTTP_201_CREATED)
async def add_event(new_event: Event):

    async with aiosqlite.connect(DB_NAME) as db:
        id_str = await mydb.event_insert(db, new_event.date, new_event.name,
         (new_event.time.hour, new_event.time.minute), new_event.location, new_event.description)
        cursor = await db.execute('''SELECT * FROM events_prod
        WHERE id = (?)
        ''', id_str)
        row = await cursor.fetchone()
        await cursor.close()

    if row is not None:
        return {"event": convert_tuple(row)}
    else: # TODO: throw an error here
        return {"event": ""}


@app.delete("/events/remove/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_event(id: UUID, should_return: bool = False):

    async with aiosqlite.connect(DB_NAME) as db:
        row = None
        if should_return:
            cursor = await db.execute('''SELECT * FROM events_prod
            WHERE id = (?)''', str(id))
            row = await cursor.fetchone()
            await cursor.close()

            if row is None:
                pass #TODO: raise error
        
        await db.execute('''DELETE FROM events_prod
        WHERE id = (?)''', str(id))

        if row is not None:
            return {"event": convert_tuple(row)}
        return {}

'''
@app.put("/events/update/{id}", status_code=status.HTTP_201_CREATED)
async def update_event(id: UUID, new_event: Event):
    db_event = fill_db_event(new_event)
    db_event.id = id
    app_db.update_event(db_event)
    return {"event": app_db.events[id]}
'''


@app.get("/events/ids/{id}")
async def get_event(id: UUID):

    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute('''SELECT * FROM events_prod
        WHERE id = (?)''', str(id))
        row = await cursor.fetchone()
        await cursor.close()

    if row is not None:
        return {"event": convert_tuple(row)}
    else: # TODO: throw an error here
        return {"event": ""}


@app.get("/events/today")
async def get_events_today():
    today: date = date.today()

    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute('''SELECT * FROM events_prod
        WHERE year = (?) AND month = (?) AND day = (?)
        ''', [today.year, today.month, today.day])
        
        rows = await cursor.fetchall()
        await cursor.close()

    return {"events": convert_tuples(rows)}


@app.get("/events/{year}/{month}/{day}")
async def get_events_date(year: int, month: int, day: int, id_only: bool = False):
    
    selector = "*"
    if id_only:
        selector = "id"
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute('''SELECT (?) FROM events_prod
        WHERE year = (?) AND month = (?) AND day = (?)
        ''', [selector, year, month, day])
        
        rows = await cursor.fetchall()
        await cursor.close()

    if id_only:
        return {"events": [{"id": elem} for elem in rows]}
    else:
        return {"events": convert_tuples(rows)}
