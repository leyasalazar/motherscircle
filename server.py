"""Server for mom events app."""

# from flask import Flask
from flask import (Flask, render_template, jsonify, request, flash, session,
                   redirect)
from model import db, connect_to_db
import crud
from datetime import datetime
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "SECRETSECRETSECRET"
app.jinja_env.undefined = StrictUndefined 

@app.route('/')
def homepage():
    """View homepage."""
    
    return render_template('homepage.html')

@app.route("/events_most_commented.json")
def show_events_most_commented():
    """View events."""
    events_most_commented = crud.events_most_commented()
    return jsonify({"events": events_most_commented})

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

@app.route("/events/<event_id>")
def individual_event(event_id):
    """View individual event."""

    event= crud.get_event_by_id(event_id)
    return render_template("event-details.html", event=event)

@app.route("/events/<event_id>/comments.json")
def get_comments_json(event_id):
    """View comments for each event."""

    comments_data = crud.get_comments_by_event(event_id)
    return jsonify({"comments": comments_data})

@app.route('/create-event')
def create_event():
    """Form to create a new event."""

    return render_template('create-event.html')    

@app.route('/add-event', methods=["POST"])
def add_event():
    """Show the events list with the new event created."""
    user_id = 1
    title = request.form.get('title')
    location = request.form.get('location')
    date = request.form.get('date')
    str_time = request.form.get('time')
    time = datetime.strptime(str_time, "%H:%M")
    description = request.form.get('description')
    img = request.form.get('img')
    if img == "":
        img = "https://i.ibb.co/zHfcq0k/chris-briggs-WNAic3c-MDR8-unsplash.jpg"

    event = crud.create_event(title, user_id, location, date, time, description, img)
    db.session.add(event)
    db.session.commit()
    # flash("Event created!")
    
    return redirect("/events")  

@app.route("/events/<event_id>/add-comment", methods=["POST"])
def add_comment(event_id):
    """Add new comment."""
    user_id = 1
    body = request.get_json().get("body")
    date = datetime.now()
    name = crud.get_name_user(user_id)
    comment = crud.create_comment(event_id, user_id, body, date)
    db.session.add(comment)
    db.session.commit()
    
    new_comment = {
        "name": name.name,
        "body": body,
        "date": str(date)
    }
    return jsonify({"success": True, "commentAdded": new_comment})

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
