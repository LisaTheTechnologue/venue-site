#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for,jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import FlaskForm
from forms import *
import sys
from flask_migrate import Migrate
from sqlalchemy import func
from datetime import datetime
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app,db)
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
#variable
todays_datetime = datetime(datetime.today().year, datetime.today().month, datetime.today().day)
#TODO: add filter to use in detail venue page
@app.template_filter('datetime')
def format_datetime(value, format="%d %b %Y %I:%M %p"):
    """Format a date time to (Default): d Mon YYYY HH:MM P"""
    if value is None:
        return ""
    return value.strftime(format)

# Genre models and connections
class Genres_venue(object):
    """
    Genres object the "genres" table.
    """
    def __init__(self, genre_id, venue_id):
        self.genre_id = genre_id
        self.venue_id = venue_id

class Genres_artist(object):
    """
    Genres object the "genres" table.
    """
    def __init__(self, genre_id, artist_id):
        self.genre_id = genre_id
        self.artist_id = artist_id

# "helper" table
genres_venue = db.Table("genres_venue",
        db.metadata,
        db.Column("id", db.Integer, primary_key = True),
        db.Column("genre_id", db.Integer, db.ForeignKey("genre.id")),
        db.Column("venue_id", db.Integer, db.ForeignKey("venue.id")),
        )

genres_artist = db.Table("genres_artist",
        db.metadata,
        db.Column("id", db.Integer, primary_key = True),
        db.Column("genre_id", db.Integer, db.ForeignKey("genre.id")),
        db.Column("artist_id", db.Integer, db.ForeignKey("artist.id")),
        )
# unique index of venue_id and genre_id
db.Index("genre_venue_link", genres_venue.c.venue_id, genres_venue.c.genre_id, unique = True)
# unique artist_id and genre_id
db.Index("genre_artist_link", genres_artist.c.artist_id, genres_artist.c.genre_id, unique = True)

class Shows(object):
    """
    Shows object the "shows" table.
    """
    def __init__(self, venue_id, artist_id):
        self.venue_id = venue_id
        self.artist_id = artist_id

shows = db.Table("shows",
        db.metadata,
        db.Column("id", db.Integer, primary_key = True),
        db.Column("venue_id", db.Integer, db.ForeignKey("venue.id")),
        db.Column("artist_id", db.Integer, db.ForeignKey("artist.id")),
        db.Column("start_time",db.DateTime, nullable=True, default=func.now())
        )

class Venue(db.Model):
    __tablename__ = "venue"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    city = db.Column(db.String(10))
    state = db.Column(db.String(2))
    address = db.Column(db.String(100))
    phone = db.Column(db.String(10))
    seeking_talent = db.Column(db.Boolean,nullable=True)
    image_link = db.Column(db.String(100))
    facebook_link =db.Column(db.String(100))
    website = db.Column(db.String(100))
    genres = db.relationship("Genre",
            secondary=genres_venue,
            backref=db.backref("venues", lazy="dynamic"),
            )
    artists = db.relationship("Artist",
            secondary=shows,
            backref=db.backref("venues", lazy="dynamic"),
            )

class Artist(db.Model):
    __tablename__ = "artist"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    address = db.Column(db.String(100))
    phone = db.Column(db.String(10))
    image_link = db.Column(db.String(100))
    facebook_link =db.Column(db.String(100))
    website = db.Column(db.String(100))
    genres = db.relationship("Genre",
            secondary=genres_artist,
            backref=db.backref("artists", lazy="dynamic"),
            )

class Genre(db.Model):
    """
    Genre table receives backref to "venues" when a "Venue" entry is created.
    """
    __tablename__ = "genre"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique=True, nullable=False)


db.mapper(Genres_venue, genres_venue)
db.mapper(Genres_artist, genres_artist)

db.mapper(Shows, shows)

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
  try:        
    citystates = db.session.query(Venue.city,Venue.state).group_by(Venue.city,Venue.state).all()
    venues = db.session.query(Venue)      
    d=[]
    for citystate in citystates:
      d1={}
      d1['city'] = citystate.city
      d1['state'] = citystate.state
      venues_data = venues.filter(Venue.city==citystate.city,Venue.state==citystate.state).all()
      d1['venues']=[]
      v=[]
      for venue in venues_data:                
          v1={}
          v1['id']=venue.id
          v1['name']=venue.name
          v1['num_upcoming_shows']= 0 #TODO: test passed but not in this app, func no attribute 'c', db.session.query(db.func.count(shows.c.id)).filter(shows.c.start_time>todays_datetime,Venue.id==venue.id).all()
          v.append(v1)
          print(v1['num_upcoming_shows'])
      d1['venues']=v
      
      d.append(d1)
    print(d)
    return render_template('pages/venues.html', areas=d)
  except Exception as error:
      return(str(error))

#TODO: edit search venue according to new schema
@app.route('/venues/search', methods=['POST'])
def search_venues():
  try:
    search_term=request.form.get('search_term', '')
    # stmt = db.session.query(shows.venue_id,func.count('*').label('num_shows_count')).filter(shows.start_time>datetime.datetime.now()).group_by(Shows.venue_id).subquery()
    query=db.session.query(Venue).filter(func.lower(Venue.name).contains(search_term.lower(), autoescape=True) )
    datas = query.all()
    response={
      "count": query.count(),
      "data": [{
        "id": data.id,
        "name": data.name,
        "num_upcoming_shows": db.session.query(db.func.count(shows.c.id)).filter(shows.c.start_time>todays_datetime,Venue.id==data.id).all()
      } for data in datas]
    }
    return render_template('pages/search_venues.html', results=response,search_term=request.form.get('search_term', ''))
  except Exception as e:
    flash(e)
    return render_template('errors/500.html')
  
@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  try:
    q=db.session.query(Venue).join(shows).filter(Venue.id==venue_id).one()
    ps=db.session.query(shows.c.artist_id).join(Venue).filter(shows.c.venue_id==venue_id,shows.c.start_time<todays_datetime).all()
    us=db.session.query(shows.c.artist_id).join(Venue).filter(shows.c.venue_id==venue_id,shows.c.start_time>=todays_datetime).all()
    aps = db.session.query(Artist,shows.c.start_time).filter(Artist.id.in_(ps)).join(shows).all()
    aus = db.session.query(Artist,shows.c.start_time).filter(Artist.id.in_(us)).all()
    
    results= {}
    results["id"]= q.id   
    results["name"]= q.name,
    results["genres"]= [ result.name for result in db.session.query(Genre.name).join(genres_venue).filter(genres_venue.c.venue_id==venue_id).all()]
    results["address"]=q.address
    results["city"]= q.city
    results["state"]= q.state
    results["phone"]= q.phone
    results["website"]= q.website
    results["facebook_link"]= q.facebook_link
    results["seeking_talent"]= q.seeking_talent
    results["image_link"]= q.image_link
    
    # past show
    results["past_shows"]= []
    print('ok')
    l=[]
    for pastshows in aps:                
        v1={}
        v1['artist_id']=pastshows.Artist.id
        v1['artist_name']=pastshows.Artist.name
        v1["artist_image_link"]= pastshows.Artist.image_link
        v1['start_time']=pastshows.start_time
        l.append(v1)
    results["past_shows"]=l
    # upcoming shows
    results["upcoming_shows"]= []
    l2=[]
    for upshows in aus:                
        v1={}
        v1['artist_id']=upshows.Artist.id
        v1['artist_name']=upshows.Artist.name
        v1['start_time']=upshows.start_time
        l2.append(v1)        
    results["upcoming_shows"]= l2
    results["past_shows_count"]= 1, #TODO: count properly
    results["upcoming_shows_count"]= 2,
    
    return render_template('pages/show_venue.html', venue=results)
  except Exception as e:
    # print('error')
    flash(e)
    return render_template('errors/500.html')
    # return(str(e))




#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  error = False
  body = {}
  try:
    # TODO: insert form data as a new Venue record in the db, instead
    name = request.get_json()['name']
    city = request.get_json()['city']
    state = request.get_json()['state']
    address = request.get_json()['address']
    phone = request.get_json()['phone']
    image_link = request.get_json()['image_link']
    facebook_link = request.get_json()['facebook_link']
    venue = Venue(name=name,city=city,state=state,address=address,phone=phone,image_link=image_link,facebook_link=facebook_link)
    print('add')
    #active_list = TodoList.query.get(list_id)
    #todo.list = active_list
    db.session.add(venue)
    db.session.commit()
    # TODO: modify data to be the data object returned from db insertion
    body['name'] = venue.name
    flash('Venue ' + venue.name + ' was successfully listed!')
    return jsonify(body)
  except Exception as e:
    flash('An error occurred. Venue could not be listed.')
    print(e)
    db.session.rollback()
    return render_template('errors/500.html')
  finally:
    db.session.close()
  
@app.route('/venues/<venue_id>', methods=['DELETE'])
#https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html#deleting-rows-from-the-many-to-many-table
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  flash("deleted")
  return None
  # try:
  #   Venue.query.filter_by(id=venue_id).delete()
  #   db.session.commit()
  # except:
  #   db.session.rollback()
  # finally:
  #   db.session.close()
  # return jsonify({ 'success': True })

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data=[{
    "id": 4,
    "name": "Guns N Petals",
  }, {
    "id": 5,
    "name": "Matt Quevedo",
  }, {
    "id": 6,
    "name": "The Wild Sax Band",
  }]
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  try:
    search_term=request.form.get('search_term', '')
    
    query=db.session.query(Artist).filter(func.lower(Artist.name).contains(search_term.lower(), autoescape=True) )
    datas = query.all()
    response={
      "count": query.count(),
      "data": [{
        "id": data.id,
        "name": data.name,
        "num_upcoming_shows": 0,
      } for data in datas]
    }
    return render_template('pages/search_artists.html', results=response,search_term=request.form.get('search_term', ''))
  except Exception as e:
    flash(e)
    return render_template('errors/500.html')

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  data1={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    "past_shows": [{
      "venue_id": 1,
      "venue_name": "The Musical Hop",
      "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
      "start_time": "2019-05-21T21:30:00.000Z"
    }],
    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
  }
  data2={
    "id": 5,
    "name": "Matt Quevedo",
    "genres": ["Jazz"],
    "city": "New York",
    "state": "NY",
    "phone": "300-400-5000",
    "facebook_link": "https://www.facebook.com/mattquevedo923251523",
    "seeking_venue": False,
    "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    "past_shows": [{
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2019-06-15T23:00:00.000Z"
    }],
    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
  }
  data3={
    "id": 6,
    "name": "The Wild Sax Band",
    "genres": ["Jazz", "Classical"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "432-325-5432",
    "seeking_venue": False,
    "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "past_shows": [],
    "upcoming_shows": [{
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2035-04-01T20:00:00.000Z"
    }, {
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2035-04-08T20:00:00.000Z"
    }, {
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2035-04-15T20:00:00.000Z"
    }],
    "past_shows_count": 0,
    "upcoming_shows_count": 3,
  }
  data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  error = False
  body = {}
  try:
    # TODO: insert form data as a new Artist record in the db, instead
    name = request.get_json()['name']
    city = request.get_json()['city']
    state = request.get_json()['state']
    address = request.get_json()['address']
    phone = request.get_json()['phone']
    genres = request.get_json()['genres']
    image_link = request.get_json()['image_link']
    facebook_link = request.get_json()['facebook_link']
    artist = Artist(name=name,city=city,state=state,address=address,phone=phone,genres=genres,image_link=image_link,facebook_link=facebook_link)
    #active_list = TodoList.query.get(list_id)
    #todo.list = active_list
    db.session.add(artist)
    db.session.commit()
    # TODO: modify data to be the data object returned from db insertion
    body['name'] = artist.name
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if not error:
    # on successful db insert, flash success
    flash('Artist ' + artist.name + ' was successfully listed!')
    return jsonify(body)
  else:
    # TODO: on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Artist ' + artist.name + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('errors/500.html')
  
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data=[{
    "venue_id": 1,
    "venue_name": "The Musical Hop",
    "artist_id": 4,
    "artist_name": "Guns N Petals",
    "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    "start_time": "2019-05-21T21:30:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 5,
    "artist_name": "Matt Quevedo",
    "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    "start_time": "2019-06-15T23:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-01T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-08T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-15T20:00:00.000Z"
  }]
  return render_template('pages/shows.html', shows=data)

# Create show
@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  error = False
  body = {}
  try:
    # TODO: insert form data as a new Show record in the db, instead
    artist_id = request.get_json('artist_id')
    venue_id = request.get_json('venue_id')
    show = shows(artist_id=artist_id,venue_id=venue_id)
    db.session.add(show)
    db.session.commit()
    # TODO: modify data to be the data object returned from db insertion
    body['name'] = show.name
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if not error:
    # on successful db insert, flash success
    flash('Show ' + show.name + ' was successfully listed!')
    return jsonify(body)
  else:
    # TODO: on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('errors/500.html')
  
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
