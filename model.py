from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """A user."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    
    events = db.relationship("Event", back_populates="user")
    comments = db.relationship("Comment", back_populates="user")
    attendees = db.relationship("Attendee", back_populates="user")

    def __repr__(self):
        return f'<User user_id={self.user_id} name={self.name}>'
        
    def get_id(self):
           return (self.user_id)


class Event(db.Model):
    """An event."""

    __tablename__ = 'events'

    event_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.user_id"),
                        nullable=False)
    location = db.Column(db.String, nullable=False)
    datetime = db.Column(db.DateTime, nullable=False)
    # time = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text)
    img = db.Column(db.String)

    user = db.relationship("User", back_populates="events")
    comments = db.relationship("Comment", back_populates="event")
    attendees = db.relationship("Attendee", back_populates="event")

    def __repr__(self):
        return f'<Event event_id={self.event_id} title={self.title}>'

    def as_dic(self):
        """Return a dict with keys as attributes and values as their values"""
        match_dict = {
            "event_id": self.event_id,
            "title": self.title,
            "user_id": self.user_id,
            "location": self.location,
            "datetime": self.datetime,
            "description": self.description,
            "img": self.img
        }
        return match_dict

class Comment(db.Model):
    """A comment."""

    __tablename__ = 'comments'

    comment_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    event_id = db.Column(db.Integer,
                         db.ForeignKey("events.event_id"),
                         nullable=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.user_id"),
                        nullable=False)
    body = db.Column(db.Text, nullable=False)
    datetime = db.Column(db.DateTime)

    event = db.relationship("Event", back_populates="comments")
    user = db.relationship("User", back_populates="comments")

    def __repr__(self):
        return f'<Comment comment_id={self.comment_id} event_id={self.event_id}>'

class Attendee(db.Model):
    """A comment."""

    __tablename__ = 'attendees'

    attendee_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    event_id = db.Column(db.Integer,
                         db.ForeignKey("events.event_id"),
                         nullable=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.user_id"),
                        nullable=False)

    event = db.relationship("Event", back_populates="attendees")
    user = db.relationship("User", back_populates="attendees")

    def __repr__(self):
        return f'<Attendee attendee_id={self.attendee_id} event_id={self.event_id}>'


def example_data():
    """Create some sample data."""

    # In case this is run more than once, empty out existing data
    User.query.delete()
    Event.query.delete()
    Comment.query.delete()
    Attendee.query.delete()

    # Add sample employees and departments

    rachel = User(email="rachel@test.com", password=generate_password_hash("123", method='sha256'), name='rachel')
    balloonicorn = User(email="balloonicorn@test.com", password=generate_password_hash("hackbright", method='sha256'), name='balloonicorn')

    ev1 = Event(title='zoo', user_id=1,location='10320 Morgan Ave S, Bloomington, MN 55431', datetime='2022-12-25 17:00', img=None)
    ev2 = Event(title='market', user_id=2,location='10320 Morgan Ave S, Bloomington, MN 55431', datetime='2022-12-16 12:00', img='example')

    comm1 = Comment(event_id=1, user_id=1, body='Nice, I am going', datetime='2022-12-25 17:00')
    comm2 = Comment(event_id=1, user_id=1, body='Nice, I am going', datetime='2022-12-25 17:00')

    att = Attendee(event_id=1,user_id=2)

    db.session.add_all([rachel, balloonicorn])
    db.session.add_all([ev1, ev2, comm1, comm2, att])
    db.session.commit()
    # try:
    #     # <use session>
    #     db.session.commit()
    # except:
    #     db.session.rollback()

def connect_to_db(app, db_uri="postgresql:///events"):
    """Connect to database."""

    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    app.config["SQLALCHEMY_ECHO"] = False
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = app
    db.init_app(app)

    


if __name__ == '__main__':
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.
    connect_to_db(app)
    print("Connected to the db!")
