"""Server for mom events app."""

# from flask import Flask
from flask import (Flask, render_template, jsonify, request, flash, session,
                   redirect)
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from model import db, connect_to_db, Event, User
import crud
from datetime import datetime
from jinja2 import StrictUndefined
from geopy import geocoders
import requests
import os

app = Flask(__name__)
app.secret_key = "SECRETSECRETSECRET"
app.jinja_env.undefined = StrictUndefined 

API_KEY = os.environ['API_KEY']

login_manager = LoginManager()
login_manager.login_view = '/login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))

@app.route('/')
def homepage():
    """View homepage."""
    
    return render_template('homepage.html')

@app.route("/events_most_commented.json")
def show_events_most_commented():
    """View events."""
    events_most_commented = crud.events_most_commented()
    return jsonify({"events": events_most_commented})

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@app.route("/login")
def login_signup():
    """Log in your account."""
    return render_template('login.html')

@app.route("/handle-login", methods=['POST'])
def handle_login():
    """Log user into application."""

    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    # check if the user actually exists
    # user = User.query.filter_by(email=email).first()
    user = crud.get_user_by_email(email)
    # print(user_info.email)
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect("/login") # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect("/")

    # if password == user_info.password:
    #     session['current_user'] = user_info.user_id
    #     print(session['current_user'])
    #     return redirect("/")
    # else:
    #     return redirect('/login')

@app.route("/signup")
def sign_up():
    """Go to sign up page."""
    return render_template('signup.html')

@app.route("/signup", methods=["POST"])
def add_user():
    """Create an account."""
    # code to validate and add user to database goes here
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email) # if this returns a user, then the email already exists in database
    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect("/signup")

     # create a new user with the form data. Hash the password so the plaintext version isn't saved.

    new_user = crud.create_user(email, generate_password_hash(password, method='sha256'), name.capitalize())
    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    # flash("User created!")

    return redirect("/login") 

@app.route('/logout')
@login_required
def logout():
    """Log out your account."""
    logout_user()
    return redirect("/")

@app.route('/events')
def show_events():
    """Show all the events."""

    return render_template('events.html')

# @app.route("/events.json")
# def get_events_json():
#     """Return a JSON response with all the events."""
    
#     return jsonify({"events": EVENT_DATA)

# @app.route("/events.json")
# def get_events_json():
#     """View events."""
#     events = crud.all_events()
#     events_data = []
#     for event in events:
#         db_event = {
#             "event_id": event.event_id,
#             "title": event.title,
#             "user_id": event.user_id,
#             "location": event.location,
#             "date": event.date,
#             "time": event.time,
#             # "description": event.description,
#             "img": event.img
#         }
#         events_data.append(db_event)
#     return jsonify({"events": events_data})

@app.route("/events.json")
def fetch_events_list():
    """View events."""
    events = Event.query.all()
    events_data = []
    for event in events:
        event_data = event.as_dic()
        event_data['user_name'] = crud.get_user_info(event_data['user_id']).name
        # print(event_data['user_name'])
        events_data.append(event_data)
    # print(events_data)
    return jsonify({"events": events_data})


@app.route("/events/<event_id>")
def individual_event(event_id):
    """View individual event."""

    event= crud.get_event_by_id(event_id)
    name = crud.get_user_info(event.user_id)
    location = event.location
    #geocodes from geopy to get lattitude and longitude
    g = geocoders.GoogleV3(API_KEY)

    place, (lat, lng) = g.geocode(location)

    response = requests.get(f'https://api.weather.gov/points/{lat},{lng}')

    results = response.json()
    url = results['properties']['forecast']
    res_forecast = requests.get(url)
    data = res_forecast.json()
    weather_info_now = data['properties']['periods'][0]

    #get attendees
    total_attendees = crud.get_total_attendees(event_id)
    #check attendee
    if current_user.is_authenticated :
        attendee = crud.find_attendance(event_id, current_user.user_id)
        # print(attendee.user_id)
    else: 
        attendee = None

    return render_template("event-details.html", event=event,name=name, data=weather_info_now, api_key=API_KEY, total_attendees=total_attendees, attendee=attendee)

@app.route("/attendance", methods=["POST"])
def attendance():
    """Update attedance"""
    attendance = request.json.get("attendance")
    event_id = request.json.get('event_id')
    
    attendee = crud.find_attendance(event_id, current_user.user_id)

    if attendance == 'going' and not attendee:
        attendee = crud.create_attendee(event_id, current_user.user_id)
        # add the new attendee to the database
        db.session.add(attendee)
        db.session.commit()
    else:
        db.session.delete(attendee)
        db.session.commit()

    return {
        "success": True, 
        "status": f"You're {attendance} to this event.",
        "total_attendees": crud.get_total_attendees(event_id)}

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
    """Add event info to the database"""
    user_id = current_user.user_id
    title = request.form.get('title')
    location = request.form.get('location')
    date = request.form.get('date')
    time = request.form.get('time')
    datetime = date+' '+time
    description = request.form.get('description')
    img = request.form.get('img')
    if img == "":
        img = "https://i.ibb.co/zHfcq0k/chris-briggs-WNAic3c-MDR8-unsplash.jpg"

    event = crud.create_event(title, user_id, location, datetime, description, img)
    db.session.add(event)
    db.session.commit()
    # flash("Event created!")
    
    return redirect("/events")  

@app.route("/events/<event_id>/add-comment", methods=["POST"])
def add_comment(event_id):
    """Add new comment."""
    user_id = current_user.user_id
    body = request.get_json().get("body")
    datetime = datetime.now()
    name = crud.get_user_info(user_id)
    comment = crud.create_comment(event_id, user_id, body, datetime)
    db.session.add(comment)
    db.session.commit()
    
    new_comment = {
        "name": name.name.capitalize(),
        "body": body,
        "date": datetime
    }
    return jsonify({"success": True, "commentAdded": new_comment})



if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
