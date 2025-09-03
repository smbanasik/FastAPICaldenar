# Fast API Calendar

## Overview

This is a project to help me learn FastAPI and get more practice with SQL, with some practical application. This project allows the user to create a FastAPI service and database to create, store, query, and delete events for a calendar.

## Features

Currently the project allows for creating, listing, and deleting events, as well as listing the current time.

### Planned

Once I rewrite the test file for the new backend, I plan on tackling the below:

- Error handling for the db and api
- Tests related to properly handling errors
- Additional query functionality (events for a specific month or specific year)

While I would like to do recurring events, I would need to think of a system to handle that without brute force replicating events.

## Tech Stack

My calendar is coded in Python, making use of Fast API to provide a web service and aiosqlite to store data. 
I use pytest to examine the API and ensure the results are what I expect.

## To Use

Usage is simple, download the repository and create a virtual environment using venv. From there install fastapi as recommended on their website: `pip install "fastapi[standard]"`, and finally install aiosqlite.

Finally, put `fastapi dev main.py` into the terminal to start the service. FastAPI provides documentation to the service, which can be viewed to explore what the calendar is capable of.

## Learning Notes

This project has been valuable in showing me the basics of how an API works, as well as providing me with additional experience in using SQL and python. I would like to look at some best practices, since there is a lot of flexibility in creating an interface.