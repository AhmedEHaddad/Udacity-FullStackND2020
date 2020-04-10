from flask_sqlalchemy import SQLAlchemy
#from config import 
from config import app, db, migrate
from datetime import datetime
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

'''shows = db.Table('show_performances',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('artist_id', db.Integer, db.ForeignKey('artist.id'), primary_key=True),
    db.Column('venue_id', db.Integer, db.ForeignKey('venue.id'), primary_key=True),
    db.Column('start_time', db.DateTime, nullable=False, default=datetime.utcnow)
)'''

class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(200))
    shows = db.relationship('Show', backref='venue', lazy=True, cascade="all, delete-orphan")

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    #artists = db.relationship('Artist', secondary=show_performances,
      #backref=db.backref('venues', lazy=True))
      
    @property
    def upcoming_shows(self):
        """
        Returns a list of upcoming shows
        """
        current_time = datetime.now()
        shows_list = self.shows
        upcoming_shows = [show for show in shows_list if show.start_time >= current_time]
        upcoming_shows_list = []
        for show in upcoming_shows:
          show_dict = {
            'artist_id': show.artist_id,
            'artist_name': show.artist.name,
            'artist_image_link': show.artist.image_link,
            'start_time': str(show.start_time),
            }
          upcoming_shows_list.append(show_dict)
        return upcoming_shows_list

    @property
    def num_up_shows(self):
        """
        Returns the number of upcoming shows
        """
        upcoming_shows = self.upcoming_shows
        return len(upcoming_shows)
  
    @property
    def past_shows(self):
        """
        Returns a list of past shows
        """
        current_time = datetime.now()
        past_shows = [show for show in self.shows if show.start_time < current_time]
        past_shows_list = []
        for show in past_shows:
          show_dict = {
            'artist_id': show.artist_id,
            'artist_name': show.artist.name,
            'artist_image_link': show.artist.image_link,
            'start_time': str(show.start_time),
            }
          past_shows_list.append(show_dict)
        return past_shows_list

    @property
    def past_shows_count(self):
        """
        Returns number of past shows
        """
        return len(self.past_shows)

    def __repr__(self):
        s = f'<Venue id: {self.id}, name: {self.name}, city: {self.city}, >' 
        return s


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
    shows = db.relationship('Show', backref='artist', lazy=True, cascade="all, delete-orphan")

    # TODO: implement any missing fields, as a database migration using Flask-Migrate


    @property
    def upcoming_shows(self):
        """
        Returns a list of upcoming shows
        """
        current_time = datetime.now()
        upcoming_shows = [show for show in self.shows if show.start_time > current_time]
        upcoming_show_list = []
        for show in upcoming_shows:
          show_dict = {
            'venue_id':show.venue_id,
            'venue_name':show.venue.name,
            'venue_image_link': show.venue.image_link,
            'venue_image_link': show.artist.image_link,
            'start_time': str(show.start_time),
          }
          upcoming_show_list.append(show_dict)
        return upcoming_show_list

    @property
    def past_shows(self):
        """
        Returns a list of past shows
        """
        current_time = datetime.now()
        past_shows = [show for show in self.shows if show.start_time < current_time]
        past_shows_list = []
        for show in past_shows:
            show_dict = {
            'venue_id':show.venue_id,
            'venue_name':show.venue.name,
            'venue_image_link': show.venue.image_link,
            'start_time': str(show.start_time),
            }
            past_shows_list.append(show_dict)
        return past_shows_list

    @property
    def past_shows_count(self):
        """
        Returns number of past shows
        """
        return len(self.past_shows)

    @property
    def unum_up_shows(self):
        """
        Returns number of upcoming shows
        """
        return len(self.upcoming_shows)

    def __repr__(self):
          s = f'<Artist id: {self.id}, name: {self.name}, city: {self.city},state: {self.state} ' \
            # + f'state: {self.state}, phone: {self.phone}, genres: {self.genres}, ' \
            # + f'shows: {self.shows}>\n'
          return s

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
class Show(db.Model):
    __tablename__ = 'shows'

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'))
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'))
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
          s = f'<Show id: {self.id}, venue_id: {self.venue_id}, artist_id: {self.artist_id}, '  \
              + f'start_time: {self.start_time}>\n'
          return s