import sqlite3
from typing import List, Tuple
from datetime import date
from uuid import UUID, uuid4

con = sqlite3.connect("calendar.db")
cursor = con.cursor()

def table_create(cursor, table_name: str, columns: List[str]):
    columns_string = ", ".join(columns)
    cursor.execute("CREATE TABLE IF NOT EXISTS " + 
    table_name + "(" + columns_string +")")

def event_insert(cursor, date: date, name: str, time: Tuple[int, int] | None, location: str | None, description: str | None):
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
    cursor.execute("INSERT INTO events VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", event_details)

table_create(cursor, "events", 
["id TEXT PRIMARY KEY", "year INTEGER NOT NULL", "month INTEGER NOT NULL",
 "day INTEGER NOT NULL", "hour INTEGER", "minutes INTEGER",
  "name TEXT NOT NULL", "location TEXT", "description TEXT"])

res = cursor.execute("SELECT name FROM sqlite_master")
print(res.fetchone())

event_insert(cursor, date.today(), "test", None, None, None)

res = cursor.execute("SELECT * FROM events")
print(res.fetchone())
