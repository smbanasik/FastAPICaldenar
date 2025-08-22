from datetime import date, timedelta, datetime
from uuid import UUID
import random as rd
import json

from fastapi.testclient import TestClient
from fastapi import status

from .main import app, app_db

from .database import DataBase as DbDataBase
from .database import Event as DbEvent

client = TestClient(app)

def create_test_events(my_database: DbDataBase):
    event_today = DbEvent("Walk the dog")
    event_today.date = date.today()
    event_today.time = datetime.now().time()
    event_today.description = "Don't forget the leash and bags"
    event_today.location = "The neighborhood"
    event_today.id = UUID(int=rd.getrandbits(128), version=4)

    event_tomorrow = DbEvent("Grocery Store Trip")
    event_tomorrow.date = date.today() + timedelta(days=1)
    event_tomorrow.id = UUID(int=rd.getrandbits(128), version=4)

    my_database._add_event_with_id_(event_today)
    my_database._add_event_with_id_(event_tomorrow)

def wipe_database(my_database: DbDataBase):
    my_database.events.clear()
    my_database.dates.clear()

def test_read_root():
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK

def test_read_today():
    create_test_events(app_db)
    response = client.get("/today")
    assert response.status_code == status.HTTP_200_OK
    js = response.json()
    assert len(js["events"]) == 1
    assert js["events"][0]["name"] == "Walk the dog"
    wipe_database(app_db)

def test_read_events():
    create_test_events(app_db)
    response = client.get("/events")
    js = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert len(js["events"]) == 2
    assert js["events"][0]["name"] == "Walk the dog"
    assert js["events"][1]["name"] == "Grocery Store Trip"
    wipe_database(app_db)

def test_read_event_ids():
    create_test_events(app_db)
    response = client.get("/events/ids")
    js = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert len(js["ids"]) == 2
    wipe_database(app_db)

def test_create_event():
    create_test_events(app_db)
    response = client.post("/events/new", json={
    "date": "2025-08-22", 
    "time": "19:10:37", 
    "name": "Take medication", 
    "description": "Take the odd numbered ones today.",
    "location": "home"
    })
    assert response.status_code == status.HTTP_201_CREATED
    assert len(app_db.events) == 3
    wipe_database(app_db)

def test_delete_event():
    create_test_events(app_db)
    response = client.get("/events/ids")
    js = response.json()
    id_remove = js["ids"][0]
    response = client.delete("/events/remove/" + str(id_remove))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert len(app_db.events) == 1
    wipe_database(app_db)

def test_update_event():
    create_test_events(app_db)
    response = client.get("/events")
    js = response.json()
    event = js["events"][0]
    event["name"] = "Take medication"
    event["location"] = "At home"
    response = client.put("/events/update/" + str(event["id"]), json=event)
    assert response.status_code == status.HTTP_201_CREATED
    response = client.get("/today")
    js = response.json()
    event = js["events"][0]
    assert event["name"] == "Take medication"
    wipe_database(app_db)

def test_read_event():
    create_test_events(app_db)
    response = client.get("/events/ids")
    js = response.json()
    id = js["ids"][0]
    response = client.get("/events/ids/" + str(id))
    js = response.json()
    assert response.status_code == status.HTTP_200_OK
    event = js["event"]
    assert event["name"] == "Walk the dog"
    wipe_database(app_db)

def test_read_events_today():
    create_test_events(app_db)
    response = client.get("/today")
    js = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert len(js["events"]) == 1
    wipe_database(app_db)

def test_read_event_date():
    create_test_events(app_db)
    my_date = date.today()
    response = client.get("/events/" + str(my_date.year) + "/" + str(my_date.month) + "/" + str(my_date.day))
    js = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert js["events"][0]["name"] == "Walk the dog"
    id = js["events"][0]["id"]
    response = client.get("/events/" + str(my_date.year) + "/" + str(my_date.month) + "/" + str(my_date.day) + "?id_only=true")
    js = response.json()
    assert js["events"][0]["id"] == id
    wipe_database(app_db)