#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

from config import *
#app = Flask(__name__)
#moment = Moment(app)
app.config.from_object('config')
#db = SQLAlchemy(app)

# TODO: connect to a local postgresql database
#migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

from models import *


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  
  #current_time = datetime.now().strftime('%Y-%m-%d %H:%S:%M')
  

  data2 = []
  cities = []
  for venue in Venue.query.distinct(Venue.city):
    if venue.city not in cities:
      city_venues = Venue.query.filter_by(city = venue.city).all()
      venues = []
      city_dict = {
      'city': venue.city,
      'state': venue.state,
      'venues': city_venues
      }
      data2.append(city_dict)

  return render_template('pages/venues.html', areas = data2)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"


  search_term=request.form.get('search_term', '')
  venues = Venue.query.filter(Venue.name.ilike('%'+search_term+'%')).all()
  data = []
  for v in venues:
    v_dict = {
      "id": v.id,
      "name": v.name,
      "num_upcoming_shows": v.num_up_shows,
    }
    data.append(v_dict)
  response2={
    "count": len(venues),
    "data": data
  }
  
  return render_template('pages/search_venues.html', results=response2, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  
  try:
    v = Venue.query.filter_by(id = venue_id).one()
  except sqlalchemy.orm.exc.NoResultFound as notfound:
    print('venue id does not exit ')
  except sqlalchemy.orm.exc.MultipleResultsFound as multipleResultsFound:
    print('Error: multiple entries with the same id ')


  return render_template('pages/show_venue.html', venue=v)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  error = False
  try:
    venue = Venue(
      name = request.form.get('name'),
      city= request.form.get('city'),
      state=request.form.get('state'),
      address=request.form.get('address'),
      phone=request.form.get('phone'),
      geners = request.form.get('geners'),
      facebook_link =request.form.get('facebook_link')
      )
    db.session.add(venue)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    flash('something went wrong: Venue ' + request.form['name'] + ' was not created!')
  finally:
    db.session.close()
  if error:
    abort (400)
  else:   
  # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  error = False
  try:
    name = Venue.query.filter_by(id=venue_id).one().name
    Venue.query.filter_by(id=venue_id).delete()
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    flash('something went wrong!')
  finally:
    db.session.close()
  if error:
    abort (400)
  else:
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
    flash('Venue: '+name +'with id' + str(venue_id) + ' was successfully listed!')
    #return None
    return redirect(url_for('index'))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database

  artsts = Artist.query.all()
  return render_template('pages/artists.html', artists=artsts)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  
  search_termm=request.form.get('search_term', '')
  artists = Artist.query.filter(Artist.name.ilike('%'+search_termm+'%')).all()
  data = []
  for a in artists:
    a_dict = {
      "id": a.id,
      "name": a.name,
      "num_upcoming_shows": a.num_up_shows,
    }
    data.append(a_dict)
  response2={
    "count": len(data),
    "data": data
  }

  return render_template('pages/search_artists.html', results=response2, search_term=search_termm)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  
  #data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0] #id's are 1,2,3 after databse populations not 4,5,6
  artst = Artist.query.filter_by(id = artist_id).one()
  return render_template('pages/show_artist.html', artist=artst)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  
  artist1 = Artist.query.filter_by(id = artist_id).one()
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist1)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  #form = ArtistForm()
  error = False
  try:
    artist = Artist.query.filter_by(id=artist_id).one()
    '''
    artist.name = request.form.get(name)
    artist.city = request.form.get(city)
    artist.state = request.form.get(state)
    artist.phone = request.form.get(phone)
    artist.genres = request.form.get(genres)
    artist.facebook_link = request.form.get(facebook_link)
    db.session.commit()
    '''
    setattr(artist, 'name', request.form['name'])
    setattr(artist, 'genres', request.form.getlist('genres'))
    #setattr(artist, 'genres', request.form.get('genres'))
    setattr(artist, 'city', request.form['city'])
    setattr(artist, 'state', request.form['state'])
    setattr(artist, 'phone', request.form['phone'])
    #setattr(artist, 'website', request.form['website'])
    setattr(artist, 'facebook_link', request.form['facebook_link'])
    #setattr(artist, 'image_link', request.form['image_link'])
    #setattr(artist, 'seeking_description', seeking_description)
    #setattr(artist, 'seeking_venue', seeking_venue)
    #Artist.update(artist)
    
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    flash('something went wrong!')
  finally:
    db.session.close()
  if error:
    abort (400)
  else:
    flash('Artist: '+artist.name +'with id:' + str(artist_id) + ' was successfully edited!')
    return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  
  venue2 = Venue.query.filter_by(id = venue_id).one()
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue2)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  error = False
  try:
    venue = Venue.query.filter_by(id=venue_id).one()
    '''
    venue.name = request.form.get(name)
    venue.city = request.form.get(city)
    venue.state = request.form.get(state)
    venue.phone = request.form.get(phone)
    venue.address = request.form.get(address)
    venue.genres = request.form.get(genres)
    venue.facebook_link = request.form.get(facebook_link)
    db.session.commit()

    '''
    setattr(venue, 'name', request.form['name'])
    setattr(venue, 'genres', request.form.getlist('genres'))
    setattr(venue, 'city', request.form['city'])
    setattr(venue, 'address', request.form['address'])
    setattr(venue, 'state', request.form['state'])
    setattr(venue, 'phone', request.form['phone'])
    #setattr(venue, 'website', request.form['website'])
    setattr(venue, 'facebook_link', request.form['facebook_link'])
    #setattr(venue, 'image_link', request.form['image_link'])
    #setattr(venue, 'seeking_description', seeking_description)
    #setattr(venue, 'seeking_venue', seeking_venue)
    #Venue.update(venue)
    #db.session.add(venue)
    
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    flash('something went wrong!')
  finally:
    db.session.close()
  if error:
    abort (400)
  else:
    flash('Venue: '+venue.name +' with id: ' + str(venue_id) + ' was successfully edited!')
    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  error = False
  try:
    '''
    artist = Artist(
      name = request.form.get('name'),
      city= request.form.get('city'),
      state=request.form.get('state'),
      #address=request.form.get('address'),
      phone=request.form.get('phone'),
      geners = request.form.getlist('genres'),
      facebook_link =request.form.get('facebook_link'),
      )
    db.session.add(artist)
    db.session.commit()
    '''
    new_artist = Artist(
      name=request.form['name'],
      genres=request.form['genres'],
      city=request.form['city'],
      state= request.form['state'],
      phone=request.form['phone'],
      #website=request.form['website'],
      #image_link=request.form['image_link'],
      facebook_link=request.form['facebook_link'],
      #seeking_venue=seeking_venue,
      #seeking_description=seeking_description,
    )
    db.session.add(new_artist)
    db.session.commit()
    
  except:
    error = True
    db.session.rollback()
    flash('something went wrong: Artist ' + request.form['name'] + ' was not created!')
  finally:
    db.session.close()
  
  if error:
    abort (400)
  else:
  # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    return render_template('pages/home.html')
    
  #return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  
  shws = Show.query.all()
  data2 = []
  for shw in Show.query.all():
    strt_time = str(shw.start_time)
    shw_dict = {
    'venue_id': shw.venue.id,
    'venue_name': shw.venue.name,
    'artist_id': shw.artist.id,
    "artist_name": shw.artist.name,
    "artist_image_link": shw.artist.image_link,
    "start_time": strt_time
    }
    data2.append(shw_dict)

  return render_template('pages/shows.html', shows=data2)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  error = False
  try:
    shw = Show(
      artist_id = request.form.get('artist_id'),
      venue_id= request.form.get('venue_id'),
      start_time=request.form.get('start_time')
      )
    db.session.add(shw)
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    flash('something went wrong: Show was not created!')
  finally:
    db.session.close()
  if error:
    abort (400)
  else:   
  # on successful db insert, flash success
    flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
