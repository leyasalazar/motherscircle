"""Script to seed database."""

import os
import json
# from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system('dropdb events')
os.system('createdb events')

model.connect_to_db(server.app)
model.db.create_all()

with open('data/users.json') as u:
    user_data = json.loads(u.read())

    # Create users, store them in list 
    users_in_db = []
    for user in user_data:
        email, password, name = (
            user["email"],
            user["password"],
            user["name"]
        )

        db_user = crud.create_user(email, password, name)
        users_in_db.append(db_user)

    model.db.session.add_all(users_in_db)
    model.db.session.commit()

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
            event["img"],
        )
        date = datetime.strptime(event["date"], "%Y-%m-%d")
        time = datetime.strptime(event["time"], "%H:%M")

        db_event = crud.create_event(title, user_id, location, date, time, description, img)
        events_in_db.append(db_event)

    model.db.session.add_all(events_in_db)
    model.db.session.commit()

with open('data/comments.json') as c:
    comment_data = json.loads(c.read())


    # Create events, store them in list 
    comments_in_db = []
    for comment in comment_data:
        event_id, user_id, body = (
            comment["event_id"],
            comment["user_id"],
            comment["body"],
        )
        date = datetime.strptime(comment["date"], "%Y-%m-%d %H:%M")

        db_comment = crud.create_comment(event_id, user_id, body, date)
        comments_in_db.append(db_comment)

    model.db.session.add_all(comments_in_db)
    model.db.session.commit()