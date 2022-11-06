"""Server for mom events app."""

# from flask import Flask
from flask import (Flask, render_template, jsonify, request, flash, session,
                   redirect)
from model import connect_to_db, db
import crud
from datetime import datetime
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "SECRETSECRETSECRET"
app.jinja_env.undefined = StrictUndefined 

EVENT_DATA = [
    {
        "title": "Zoo",
        "user_id": 1,
        "location": "Minnesota Zoo",
        "date": "2022-11-06",
        "time": "12:00",
        "description": "I am going with my son this weekend",
        "img": "https://i.ibb.co/zHfcq0k/chris-briggs-WNAic3c-MDR8-unsplash.jpg"
    },
    {
        "title": "Museum",
        "user_id": 2,
        "location": "MIA",
        "date": "2022-11-06",
        "time": "12:00",
        "description": "I am going with my daughter this weekend",
        "img": "https://i.ibb.co/zHfcq0k/chris-briggs-WNAic3c-MDR8-unsplash.jpg"
    }]

@app.route('/')
def homepage():
    """View homepage."""
    return render_template('homepage.html')

@app.route('/events')
def show_events():
    """Show all the events."""

    return render_template('events.html')

# @app.route("/events.json")
# def get_events_json():
#     """Return a JSON response with all the events."""
    
#     return jsonify({"events": EVENT_DATA)

@app.route("/events.json")
def get_events_json():
    """View events."""
    events = crud.all_events()
    events_data = []
    for event in events:
        db_event = {
            "event_id": event.event_id,
            "title": event.title,
            "user_id": event.user_id,
            "location": event.location,
            "date": event.date,
            "time": event.time,
            # "description": event.description,
            "img": event.img
        }
        events_data.append(db_event)
    print(events_data)
    return jsonify({"events": events_data})

# @app.route("/fetch_events_list")
# def fetch_events_list():
#     """View events."""
#     events = Event.query.all()
#     events_data = []
#     for event in events:
#         event_data = event.as_dict()
#         events_data.append(event_data)
#     print(events_data)
#     return jsonify({"events": events_data})

@app.route("/<event_id>")
def individual_event(event_id):
    """View individual event."""

    event= crud.get_event_by_id(event_id)
    return render_template("event_details.html", event=event)
    

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)