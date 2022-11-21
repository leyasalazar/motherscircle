from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """A user."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    
    events = db.relationship("Event", back_populates="user_create")
    comments = db.relationship("Comment", back_populates="user")

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
    date_time = db.Column(db.DateTime, nullable=False)
    # time = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text)
    img = db.Column(db.String)

    user_create = db.relationship("User", back_populates="events")
    comments = db.relationship("Comment", back_populates="event")

    def __repr__(self):
        return f'<Event event_id={self.event_id} title={self.title}>'

    def as_dic(self):
        """Return a dict with keys as attributes and values as their values"""
        match_dict = {
            "event_id": self.event_id,
            "title": self.title,
            "user_id": self.user_id,
            "location": self.location,
            "date_time": self.date_time,
            # "time": self.time,
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
    date = db.Column(db.DateTime)

    event = db.relationship("Event", back_populates="comments")
    user = db.relationship("User", back_populates="comments")

    def __repr__(self):
        return f'<Comment comment_id={self.comment_id} event_id={self.event_id}>'


def connect_to_db(app):
    """Connect to database."""

    app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql:///events"
    app.config["SQLALCHEMY_ECHO"] = False
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = app
    db.init_app(app)

    print("Connected to the db!")


if __name__ == '__main__':
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.
    connect_to_db(app)
