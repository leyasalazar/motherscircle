"""CRUD operations."""

from model import db, User, Event, Comment, connect_to_db

# Functions start here!
def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    return user

def create_event(title, user_id, location, date, time, description, img):
    """Create and return a new event."""
    event = Event(title=title, user_id=user_id, location=location, date=date, time=time, description=description, img=img)

    return event

def create_comment(event_id, user_id, body, date):
    """Create and return a new event."""
    comment = Comment(event_id=event_id, user_id=user_id, body=body, date=date)

    return comment

def all_events():
    """Return all events"""
    return Event.query.all()

def get_event_by_id(event_id):
    return Event.query.get(event_id)


if __name__ == '__main__':
    from server import app
    connect_to_db(app)