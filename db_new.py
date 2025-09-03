import aiosqlite
from typing import List, Tuple
from datetime import date
from uuid import UUID, uuid4

async def table_drop(connect: aiosqlite.Connection, table_name: str):
    await connect.execute("DROP TABLE IF EXISTS " + table_name)
    await connect.commit()

async def table_create(connect: aiosqlite.Connection, table_name: str, columns: List[str]):
    columns_string = ", ".join(columns)
    await connect.execute("CREATE TABLE IF NOT EXISTS " + 
    table_name + "(" + columns_string +")")
    await connect.commit()

async def event_insert(connect: aiosqlite.Connection, date: date, name: str, time: Tuple[int, int] | None = None, location: str | None = None, description: str | None = None):
    id_str: str = str(uuid4())
    event_details = [id_str, date.year, date.month, date.day]
    if time is not None:
        event_details.extend([time[0], time[1]])
    else:
        event_details.extend([None, None])
    event_details.append(name)
    if location is not None:
        event_details.append(location)
    else:
        event_details.append(None)
    if description is not None:
        event_details.append(description)
    else:
        event_details.append(None)
    await connect.execute("INSERT INTO events_prod VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", event_details)
    await connect.commit()
    return id_str

'''
table_create(connect, "events_prod", 
["id TEXT PRIMARY KEY", "year INTEGER NOT NULL", "month INTEGER NOT NULL",
 "day INTEGER NOT NULL", "hour INTEGER", "minutes INTEGER",
  "name TEXT NOT NULL", "location TEXT", "description TEXT"])

table_create(connect, "events_test", 
["id TEXT PRIMARY KEY", "year INTEGER NOT NULL", "month INTEGER NOT NULL",
 "day INTEGER NOT NULL", "hour INTEGER", "minutes INTEGER",
  "name TEXT NOT NULL", "location TEXT", "description TEXT"])
'''