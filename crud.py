"""CRUD operations."""

from model import db, User, Event, Comment, connect_to_db

# Functions start here!
def create_user(email, password, name):
    """Create and return a new user."""

    user = User(email=email, password=password, name=name)

    return user

def get_user_by_email(email):
    return User.query.filter_by(email=email).first()

def get_user_info(user_id):

    return User.query.get(user_id)

def get_password(email):
    user_info = User.query.filter_by(email=email)
    return user_info

def create_event(title, user_id, location, date_time, description, img):
    """Create and return a new event."""
    event = Event(title=title, user_id=user_id, location=location, date_time=date_time, description=description, img=img)

    return event

def all_events():
    """Return all events"""
    return Event.query.all()

def get_event_by_id(event_id):
    return Event.query.get(event_id)

def events_most_commented():
    """List of events more commented"""

    #SELECT event_id FROM comments GROUP BY event_id;
    #SELECT * FROM events WHERE event_id IN(SELECT event_id FROM comments GROUP BY event_id LIMIT 3);

    events = Event.query.join(db.session.query(Comment.event_id).group_by(Comment.event_id).limit(3)).all()

    events_most_commented = []
    for event in events:
        user = get_user_info(event.user_id)
        event_data = {
            "event_id": event.event_id,
            "title": event.title,
            "name": user.name,
            "location": event.location,
            "date_time": event.date_time,
            # "time": event.time, 
            "img": event.img
        }
        events_most_commented.append(event_data)
    return events_most_commented

def create_comment(event_id, user_id, body, date):
    """Create and return a new comment."""
    comment = Comment(event_id=event_id, user_id=user_id, body=body, date=date)

    return comment

def get_comments_by_event(event_id):
    """Get all the comments for the same event."""
    comments = Comment.query.filter_by(event_id=event_id).all()
    comments_by_event = []
    for comment in comments:
        user = get_user_info(comment.user_id)
        comment_data = {
            "comment_id": comment.comment_id,
            "name": user.name,
            "body": comment.body,
            "date": comment.date
        }
        comments_by_event.append(comment_data)
    return comments_by_event



if __name__ == '__main__':
    from server import app
    connect_to_db(app)