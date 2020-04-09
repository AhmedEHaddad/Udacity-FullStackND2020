from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
#from database_setup import Category, Base, Item, User
from app import Artist, Venue

engine = create_engine('postgresql://devuser:devpass@localhost:5432/fyyurDB')
 Bind the engine to the metadata of the Base class so that the
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

######## populate artists
artist1 = Artist(id=1, name="Guns N Petals")
session.add(artist1)
session.commit()

artist2 = Artist(id=2, name="Matt Quevedo")
session.add(artist2)
session.commit()

artist3 = Artist(id=3, name="The Wild Sax Band")
session.add(artist3)
session.commit()

####### populate venues



####### populate shows







print "populated the database with some dummy data!"