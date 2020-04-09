from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate



shows = db.Table('show_performances',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('artist_id', db.Integer, db.ForeignKey('artist.id'), primary_key=True),
    db.Column('venue_id', db.Integer, db.ForeignKey('venue.id'), primary_key=True),
    db.Column('start_time', db.DateTime, nullable=False, default=datetime.utcnow)
)

class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    #shows = db.relationship('Show', backref='venue', lazy=True)
    artists = db.relationship('Artist', secondary=show_performances,
      backref=db.backref('venues', lazy=True))

class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    #shows = db.relationship('Show', backref='artist', lazy=True)