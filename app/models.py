#models used for backend (data structures)

from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

#data structure/table related to each user, attained from registration page and used later for stats
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    firstname = db.Column(db.String(64))
    surname = db.Column(db.String(64))
    dob = db.Column(db.Date)
    address = db.Column(db.String(128))
    country = db.Column(db.String(64))
    state = db.Column(db.String(64))
    postcode = db.Column(db.Integer)
    phone = db.Column(db.Integer)
    email = db.Column(db.String(128), unique=True, index=True)
    balance = db.Column(db.Float)
    password_hash = db.Column(db.String(128))

#functionality for setting and checking password hashes
    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


#model for event
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    sport = db.Column(db.String(64))

    def __repr__(self):
        return '<Event {}>'.format(self.title)

#table for event result options
class Option(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pick = db.Column(db.String(64))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    colour = db.Column(db.String(64))
    accentColour = db.Column(db.String(64))

    def __repr__(self):
        return '<Option {}>'.format(self.pick)

#table for event listings
class Listing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    odds = db.Column(db.Float)
    listers_odds = db.Column(db.Float)
    amount = db.Column(db.Float)
    user_return = db.Column(db.Float)
    option_id = db.Column(db.Integer, db.ForeignKey('option.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    matched = db.Column(db.Boolean)
    datetime = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Listing {}>'.format(self.odds)


#table for matched listings not yet realised
class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_listing_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_matching_id = db.Column(db.Integer, db.ForeignKey('user.id'))

#table for matched listings which have been realised
class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey('match.id'))
    winning_user = db.Column(db.Integer, db.ForeignKey('user.id'))