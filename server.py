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

    new_user = crud.create_user(email, generate_password_hash(password, method='sha256'), name)
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
        events_data.append(event_data)
    print(events_data)
    return jsonify({"events": events_data})

# @app.route("/events/<event_id>")
# def individual_event(event_id):
#     """View individual event."""

#     event= crud.get_event_by_id(event_id)
#     return render_template("event-details.html", event=event)

@app.route("/events/<event_id>")
def individual_event(event_id):
    """View individual event."""

    event= crud.get_event_by_id(event_id)
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

    return render_template("event-details.html", event=event, data=weather_info_now, api_key=API_KEY)

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

# @app.route("/latlng", methods=["POST"])
# def get_lat_lng():
#     """Weather API."""
#     lat = request.json.get("lat")
#     lng = request.json.get("lng")
#     print(lat, lng)
#     response = requests.get(f'https://api.weather.gov/points/{lat},{lng}')

#     search_results = response.json()
#     url = search_results['properties']['forecast']
#     res_forecast = requests.get(url)
#     data = res_forecast.json()
#     print(url)
#     print(data['properties']['periods'][0])
#     specific_data = data['properties']['periods'][0]
#     return render_template('event-details.html',specific_data=specific_data)

    # return {
    #     "success": True, 
    #     "status": f'{lat} ------ {lng}'}
    # # return redirect("/events")  

# @app.route("/weather")
# def get_weather():
#     """Weather API."""
    
#     response = requests.get('https://api.weather.gov/points/44.7675046,-93.1956983')

#     search_results = response.json()
#     url = search_results['properties']['forecast']
#     res_forecast = requests.get(url)
#     data = res_forecast.json()
#     print(url)
#     print(data['properties']['periods'][0]["icon"])
#     specific_data = data['properties']['periods'][0]
#     return render_template('weather.html',specific_data=specific_data)

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
