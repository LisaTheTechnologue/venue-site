#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for,jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

import sys
from flask_migrate import Migrate
from sqlalchemy import func
import datetime
# from datetime import datetime

import logging
from logging import Formatter, FileHandler

#Flask Form
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField,BooleanField
from wtforms.validators import DataRequired, AnyOf, URL
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from forms import *


from json import JSONEncoder
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
todays_datetime = datetime.datetime.now() # datetime(datetime.today().year, datetime.today().month, datetime.today().day)

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

class Show(db.Model):
    __tablename__ = "show"
    id = db.Column(db.Integer, primary_key = True)
    venue_id =  db.Column(db.Integer, db.ForeignKey("venue.id",ondelete='CASCADE'))
    artist_id = db.Column(db.Integer, db.ForeignKey("artist.id",ondelete='CASCADE'))
    start_time = db.Column(db.DateTime, nullable=True,
        default=datetime.datetime.now())

class Venue(db.Model):
    __tablename__ = "venue"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    city = db.Column(db.String(10))
    state = db.Column(db.String(2))
    address = db.Column(db.String())
    phone = db.Column(db.String(10))
    seeking_talent = db.Column(db.Boolean,nullable=True)
    image_link = db.Column(db.String())
    facebook_link =db.Column(db.String())
    website = db.Column(db.String())
    genres = db.relationship("Genre",
            secondary=genres_venue,
            backref=db.backref("venues", lazy="dynamic"),
            )
    artists = db.relationship("Artist",
            secondary="show",
            backref=db.backref("venues", lazy="dynamic"),
            )

class Artist(db.Model):
    __tablename__ = "artist"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    city = db.Column(db.String(10))
    state = db.Column(db.String(2))
    address = db.Column(db.String())
    phone = db.Column(db.String(10))
    seeking_venue = db.Column(db.Boolean,nullable=True)
    image_link = db.Column(db.String())
    facebook_link =db.Column(db.String())
    website = db.Column(db.String())
    genres = db.relationship("Genre",
            secondary=genres_artist,
            backref=db.backref("artists", lazy="dynamic"),
            )

class Genre(db.Model):
    __tablename__ = "genre"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique=True, nullable=False)

# form choices
def genre_choices():
    return Genre.query()
######
db.mapper(Genres_venue, genres_venue)
db.mapper(Genres_artist, genres_artist)
# db.mapper(Shows, shows)

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

# subclass JSONEncoder
class DateTimeEncoder(JSONEncoder):

    def default(self, obj):
        if isinstance(obj, (datetime.datetime, datetime.date, datetime.time)):
            return obj.isoformat()
        elif isinstance(obj, datetime.timedelta):
            return (datetime.datetime.min + obj).time().isoformat()

        return super(DateTimeEncoder, self).default(obj)


######
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
        showcount = db.session.query(Show).filter(Show.start_time>todays_datetime,Venue.id==venue.id).count()
        v1={}
        v1['id']=venue.id
        v1['name']=venue.name
        v1['num_upcoming_shows']= showcount
        v.append(v1)
        print(v1['num_upcoming_shows'])
      d1['venues']=v
      
      d.append(d1)
    print(d)
    return render_template('pages/venues.html', areas=d)
  except Exception as error:
      return(str(error))

@app.route('/venues/search', methods=['POST'])
def search_venues():
  try:
    search_term=request.form.get('search_term', '')
    # stmt = db.session.query(shows.venue_id,func.count('*').label('num_shows_count')).filter(shows.start_time>datetime.datetime.now()).group_by(Shows.venue_id).subquery()
    query1=db.session.query(Venue).filter(func.lower(Venue.name).contains(search_term.lower(), autoescape=True)) 
    datas = query1.all()
    response={}
    response["count"]= query1.count()
    listdata=[]
    for data in datas:
      dictdata={}
      dictdata["id"]= data.id
      dictdata["name"]= data.name
      dictdata["num_upcoming_shows"]= db.session.query(Show).filter(Show.start_time>todays_datetime,Venue.id==data.id).count()
      listdata.append(dictdata)
    response["data"]=listdata
    response = dict(response)
    print(type(response))
    return render_template('pages/search_venues.html', results=response,search_term=request.form.get('search_term', ''))
  except Exception as e:
    flash(e)
    return render_template('errors/500.html')
  
@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  encoder = DateTimeEncoder()
  try:
    print(venue_id)
    results= {}
    q=db.session.query(Venue).filter(Venue.id==venue_id).first()
    if(q is None):
      return render_template('errors/404.html')
    else :
      aps = db.session.query(Show.start_time,Artist.id,Artist.name,Artist.image_link).join(Artist).filter(Show.artist_id==2,Show.start_time<todays_datetime).order_by(Show.start_time).all()
      aus = db.session.query(Show.start_time,Artist.id,Artist.name,Artist.image_link).join(Artist).filter(Show.artist_id==2,Show.start_time>=todays_datetime).order_by(Show.start_time).all()

      results["id"]= q.id   
      results["name"]= q.name
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
      pastcount=0
      for pastshows in aps:                
        pastcount =pastcount+1
        v1={}
        v1['artist_id']=pastshows.id
        v1['artist_name']=pastshows.name
        v1["artist_image_link"]= pastshows.image_link
        v1['start_time']=str(pastshows.start_time) 
        # v1['start_time'] = v1['start_time'].dt.strftime('%Y-%m-%d %H:%M:%S')
        l.append(v1)
      results["past_shows"]=l


      # upcoming shows
      results["upcoming_shows"]= []
      l2=[]
      upcount=0
      for upshows in aus:                
        upcount = upcount+1
        v1={}
        v1['artist_id']=upshows.id
        v1['artist_name']=upshows.name
        v1['start_time']= str(upshows.start_time)# json.dumps(upshows.start_time,default=myconverter)#encoder.encode({"datetime": upshows.start_time, "date": upshows.start_time.date(), "time": upshows.start_time.time()})
        l2.append(v1)        
      results["upcoming_shows"]= l2
      results["past_shows_count"]= pastcount
      results["upcoming_shows_count"]= upcount
      # DateTimeEncoder().encode(results)
      # format_datetime
      # json.dumps(results,default=myconverter)
      print(results)
    return render_template('pages/show_venue.html', venue = results)#venue=json.dumps(results, indent=4, sort_keys=True, default=str))
    # return json.dumps(results, indent=4, sort_keys=True, default=str)
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
  form.genres.choices = [(genre.id,genre.name) for genre in Genre.query.all()]
  return render_template('forms/new_venue.html', form=form)

#TODO: cannot added yet + add genre and seeking_talents field
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
    website = request.get_json()['website']
    seeking_talent = request.get_json()['seeking_talent']
    genres = request.get_json()['genres']
    venue = Venue(name=name,city=city,state=state,address=address,phone=phone,image_link=image_link,facebook_link=facebook_link,website=website,seeking_talent=seeking_talent)
    
    i=0
    for genre in genres:
      genre = db.session.query(Genre).get(genres[i])
      print(genre)
      venue.genres.extend([genre]) # attach the Category objects to the post   
      i=i+1 
    # venue = Venue(name=name,city=city,state=state,address=address)
    
    db.session.add(venue)
    db.session.commit()    
    body['name'] = venue.name
    
  except Exception as e:
    error = True
    print(e)
    db.session.rollback()
    
  finally:
    db.session.close()
  if not error:
    flash('Venue ' + venue.name + ' was successfully listed!')
    return jsonify(body)
  else:
    flash('An error occurred. Venue could not be listed.')
    return render_template('errors/500.html')

  return render_template('pages/home.html')


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  try:        
    # citystates = db.session.query(Venue.city,Venue.state).group_by(Venue.city,Venue.state).all()
    datas = db.session.query(Artist)      
    d=[]
      
    for data in datas:                
      v1={}
      v1['id']=data.id
      v1['name']=data.name    
      
    d.append(v1)
    print(d)
    return render_template('pages/artists.html', artists=d)
  except Exception as error:
      return(str(error))

@app.route('/artists/search', methods=['POST'])
def search_artists():
  try:
    search_term=request.form.get('search_term', '')
    # stmt = db.session.query(shows.venue_id,func.count('*').label('num_shows_count')).filter(shows.start_time>datetime.datetime.now()).group_by(Shows.venue_id).subquery()
    query1=db.session.query(Artist).filter(func.lower(Artist.name).contains(search_term.lower(), autoescape=True)) 
    datas = query1.all()
    response={}
    response["count"]= query1.count()
    listdata=[]
    for data in datas:
      dictdata={}
      dictdata["id"]= data.id
      dictdata["name"]= data.name
      dictdata["num_upcoming_shows"]= db.session.query(Show).filter(Show.start_time>todays_datetime,Artist.id==data.id).count()
      listdata.append(dictdata)
    response["data"]=listdata
    response = dict(response)
    print(type(response))
    return render_template('pages/search_artists.html', results=response,search_term=request.form.get('search_term', ''))
  except Exception as e:
    flash(e)
    return render_template('errors/500.html')

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  try:
    print(artist_id)
    results= {}
    q=db.session.query(Artist).filter(Artist.id==artist_id).first()
    if(q is None):
      return render_template('errors/404.html')
    else :
      aps = db.session.query(Show.start_time,Venue.id,Venue.name,Venue.image_link).join(Venue).filter(Show.artist_id==artist_id,Show.start_time<todays_datetime).order_by(Show.start_time).all()
      aus = db.session.query(Show.start_time,Venue.id,Venue.name,Venue.image_link).join(Venue).filter(Show.artist_id==artist_id,Show.start_time>=todays_datetime).order_by(Show.start_time).all()

      results["id"]= q.id   
      results["name"]= q.name
      results["genres"]= [ result.name for result in db.session.query(Genre.name).join(genres_artist).filter(genres_artist.c.artist_id==artist_id).all()]
      results["address"]=q.address
      results["city"]= q.city
      results["state"]= q.state
      results["phone"]= q.phone
      results["website"]= q.website
      results["facebook_link"]= q.facebook_link
      results["seeking_venue"]= q.seeking_venue
      results["image_link"]= q.image_link
      
      # past show
      results["past_shows"]= []
      print('ok')
      l=[]
      pastcount=0
      for pastshows in aps:                
        pastcount =pastcount+1
        v1={}
        v1['venue_id']=pastshows.id
        v1['venue_name']=pastshows.name
        v1["venue_image_link"]= pastshows.image_link
        v1['start_time']=str(pastshows.start_time )
        # v1['start_time'] = v1['start_time'].dt.strftime('%Y-%m-%d %H:%M:%S')
        l.append(v1)
      results["past_shows"]=l
      # upcoming shows
      results["upcoming_shows"]= []
      l2=[]
      upcount=0
      for upshows in aus:                
        upcount = upcount+1
        v1={}
        v1['venue_id']=upshows.id
        v1['venue_name']=upshows.name
        v1['start_time']=str(upshows.start_time)
        l2.append(v1)        
      results["upcoming_shows"]= l2
      results["past_shows_count"]= pastcount
      results["upcoming_shows_count"]= upcount
      # DateTimeEncoder().encode(results)
      print(results)
    return render_template('pages/show_artist.html', artist = results)#artist=json.dumps(results, indent=4, sort_keys=True, default=str))
    # return json.dumps(results, indent=4, sort_keys=True, default=str)
  except Exception as e:
    # print('error')
    flash(e)
    return render_template('errors/500.html')

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
    image_link = request.get_json()['image_link']
    facebook_link = request.get_json()['facebook_link']
    website = request.get_json()['website']
    seeking_talent = request.get_json()['seeking_talent']
    genres = request.get_json()['genres']
    artist = Artist(name=name,city=city,state=state,address=address,phone=phone,image_link=image_link,facebook_link=facebook_link,website=website,seeking_talent=seeking_talent)
    i=0
    for genre in genres:
      genre = db.session.query(Genre).get(genres[i])
      print(genre)
      artist.genres.extend([genre]) # attach the Category objects to the post   
      i=i+1 
    db.session.add(artist)
    db.session.commit()
    
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
  try:        
    # citystates = db.session.query(Venue.city,Venue.state).group_by(Venue.city,Venue.state).all()
    show_datas =  db.session.query(Show.start_time,Artist,Venue).filter(Show.venue_id==Venue.id,Show.artist_id==Artist.id).all()
    d=[]
    for show_data in show_datas:      
      v1={}
      v1['venue_id']=show_data.Venue.id
      v1['venue_name']=show_data.Venue.name
      v1['artist_id']=show_data.Artist.id
      v1['artist_name']=show_data.Artist.name
      v1['artist_image_link']=show_data.Artist.image_link
      v1['start_time']= str(show_data.start_time)
      d.append(v1)
    print(d)
    return render_template('pages/shows.html', shows=d)
  except Exception as error:
      return(str(error))

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
