from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
#from database_setup import Category, Base, Item, User
from app import Artist, Venue, Show
from flask_sqlalchemy import SQLAlchemy
from flask import Flask


"""
engine = create_engine('postgresql=//devuser=devpass@localhost=5432/fyyurDB')
#Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# items for Smartphones 
'''
category1 = Category(user_id=1, name="Smartphones")

session.add(category1)
session.commit()

item1 = Item(user_id=1, name="Huawei Mate 30", description="Huawei's 5G phone will be foldable.",
                     date=datetime.datetime.now(), price="$600", type="Smartphone", model="P30 or Mate 30", manufacturer="HUAWEI", category=category1)
'''

"""

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://devuser:devpass@localhost:5432/fyyurDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


######## populate artists
artist1 = Artist(id=1, name="Guns N Petals", genres = "Rock n Roll",
    city= "San Francisco",
    state= "CA",
    phone= "326-123-5000",
    website= "https://www.gunsnpetalsband.com",
    facebook_link= "https://www.facebook.com/GunsNPetals",
    seeking_venue= True,
    seeking_description= "Looking for shows to perform at in the San Francisco Bay Area!",
    image_link= "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
    )
db.session.add(artist1)
db.session.commit()

artist2 = Artist(id=2, name="Matt Quevedo", genres = "Jazz",
    city= "New York",
    state= "NY",
    phone= "300-400-5000",
    facebook_link= "https://www.facebook.com/mattquevedo923251523",
    seeking_venue= False,
    image_link= "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80"
    )
db.session.add(artist2)
db.session.commit()

artist3 = Artist(id=3, name="The Wild Sax Band", genres = " Jazz, Classical ",
    city= "San Francisco",
    state= "CA",
    phone= "432-325-5432",
    seeking_venue= False,
    image_link= "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80"
    )
db.session.add(artist3)
db.session.commit()


####### populate venues
venue1 = Venue(id = 1,
    name= "The Musical Hop",
    genres= '["Jazz", "Reggae", "Swing", "Classical", "Folk"]',
    address= "1015 Folsom Street",
    city= "San Francisco",
    state= "CA",
    phone= "123-123-1234",
    website= "https=//www.themusicalhop.com",
    facebook_link= "https=//www.facebook.com/TheMusicalHop",
    seeking_talent= True,
    seeking_description= "We are on the lookout for a local artist to play every two weeks. Please call us.",
    image_link= "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"

    )
db.session.add(venue1)
db.session.commit()

venue2 = Venue(id = 2,
    name= "The Dueling Pianos Bar",
    genres= '["Classical", "R&B", "Hip-Hop"]',
    address= "335 Delancey Street",
    city= "New York",
    state= "NY",
    phone= "914-003-1132",
    website= "https://www.theduelingpianos.com",
    facebook_link= "https://www.facebook.com/theduelingpianos",
    seeking_talent= False,
    image_link= "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80"

    )
db.session.add(venue2)
db.session.commit()

venue3 = Venue(id = 3,
    name= "Park Square Live Music & Coffee",
    genres= '["Rock n Roll", "Jazz", "Classical", "Folk"]',
    address= "34 Whiskey Moore Ave",
    city= "San Francisco",
    state= "CA",
    phone= "415-000-1234",
    website= "https://www.parksquarelivemusicandcoffee.com",
    facebook_link= "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
    seeking_talent= False,
    image_link= "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80"

    )
db.session.add(venue3)
db.session.commit()


####### populate shows 
show1 = Show(id = 1,venue_id = 1 ,artist_id =1,  start_time='2019-05-21T21:30:00.000Z')
db.session.add(show1)
db.session.commit()

show2 = Show(id = 2,venue_id = 3 ,artist_id =2,  start_time='2019-06-15T23:00:00.000Z')
db.session.add(show2)
db.session.commit()

show3 = Show(id = 3,venue_id = 3 ,artist_id =3,  start_time='2035-04-01T20:00:00.000Z')
db.session.add(show3)
db.session.commit()

show4 = Show(id = 4,venue_id = 3 ,artist_id =3,  start_time='2035-04-08T20:00:00.000Z')
db.session.add(show4)
db.session.commit()

show5 = Show(id = 5,venue_id = 3 ,artist_id =3,  start_time='2035-04-15T20:00:00.000Z')
db.session.add(show5)
db.session.commit()






print ("populated the database with some dummy data!")