"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system('dropdb events')
os.system('createdb events')

model.connect_to_db(server.app)
model.db.create_all()

with open('data/events.json') as f:
    event_data = json.loads(f.read())


# Create events, store them in list 
events_in_db = []
for event in event_data:
    title, user_id, location, description, img = (
        event["title"],
        event["user_id"],
        event["location"],
        event["description"],
        event["img"]
    )
    date = datetime.strptime(event["date"], "%Y-%m-%d")
    time = datetime.strptime(event["time"], "%H:%M")

    db_event = crud.create_event(title, user_id, location, date, time, description, img)
    events_in_db.append(db_event)

model.db.session.add_all(events_in_db)
model.db.session.commit()