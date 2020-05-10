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
from forms import VenueForm,ArtistForm,ShowForm


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
    seeking_description = db.Column(db.String(100))
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
    seeking_description = db.Column(db.String(100))
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

#  Venue Handlers
#  ----------------------------------------------------------------
# createvenue
@app.route('/venues/create', methods=['GET','POST'])
def create_venue_form():
  form = VenueForm()
  form.genres.choices = [(genre.id,genre.name) for genre in Genre.query.all()]
  if (request.method == 'POST') : 
    name = form.name.data    
    # Get user and group
    existname = Venue.query.filter_by(name=name).first()
    if existname is not None:
      flash("Venue exists.")
      return render_template('forms/new_venue.html', form=form)
    error = False
    body = {}
    try:
      name = request.form.get('name')
      city = request.form.get('city')
      state = request.form.get('state')
      address = request.form.get('address')
      phone = request.form.get('phone')
      image_link = request.form.get('image_link')
      facebook_link = request.form.get('facebook_link')
      website = request.form.get('website')
      
      # SEEKING TALENTS
      seeking_talent = request.form.get('seeking_talent')
      seeking_description = request.form.get('seeking_description')
        
      if(seeking_talent=='y'):
        seeking_talent = True
      else: 
        seeking_talent = False

      # CREATE
      venue = Venue(name=name,city=city,state=state,address=address,phone=phone,image_link=image_link,facebook_link=facebook_link,website=website,seeking_talent=seeking_talent,seeking_description=seeking_description)
      
      # GENRE
      genres = request.form.get('genres')
      i=0
      for genre in genres:
        genre = db.session.query(Genre).get(genres[i])
        print(genre)
        venue.genres.extend([genre])
        i=i+1 
          
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
      return redirect(url_for('venues'))
    else:
      flash('An error occurred. Venue could not be listed.')
      return render_template('errors/500.html')
  # if request method is GET then generate form
  return render_template('forms/new_venue.html', form=form)

# listvenues
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
    flash(error)
    return render_template('errors/500.html')

#searchvenues
@app.route('/venues/search', methods=['POST'])
def search_venues():
  try:
    search_term=request.form.get('search_term', '')
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

# detailvenue
@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  try:
    print(venue_id)
    results= {}
    q=db.session.query(Venue).filter(Venue.id==venue_id).first()
    if(q is None):
      return render_template('errors/404.html')
    else :
      aps = db.session.query(Show.start_time,Artist.id,Artist.name,Artist.image_link).join(Artist).filter(Show.venue_id==venue_id,Show.start_time<todays_datetime).order_by(Show.start_time).all()
      aus = db.session.query(Show.start_time,Artist.id,Artist.name,Artist.image_link).join(Artist).filter(Show.venue_id==venue_id,Show.start_time>=todays_datetime).order_by(Show.start_time).all()

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
      results["seeking_description"]= q.seeking_description
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
        v1['start_time']= str(upshows.start_time)
        l2.append(v1)        
      results["upcoming_shows"]= l2
      results["past_shows_count"]= pastcount
      results["upcoming_shows_count"]= upcount

      print(results)
    return render_template('pages/show_venue.html', venue = results)
  except Exception as e:
    flash(e)
    return render_template('errors/500.html')

# editvenue
@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  try:
    print(venue_id)
    results= {}
    q=db.session.query(Venue).filter(Venue.id==venue_id).first()
    if(q is None):
      return render_template('errors/404.html')
    else :
      genres=Genre.query.all()
      results["id"]= q.id   
      results["name"]= q.name
      results["address"]=q.address
      results["city"]= q.city
      results["state"]= q.state
      results["phone"]= q.phone
      results["website"]= q.website
      results["facebook_link"]= q.facebook_link
      results["seeking_talent"]= q.seeking_talent
      results["seeking_description"]=q.seeking_description
      results["image_link"]= q.image_link      
      
      # populate form with existed data
      form = VenueForm(data=results)
      form.genres.choices = [(genre.id,genre.name) for genre in Genre.query.all()]
      v=[]
      for g in q.genres:
        v.append(str(g.id))
      genres_populate = v
      print(genres_populate)
      form.genres.data = genres_populate 
    return render_template('forms/edit_venue.html', form=form, venue=results)
  except Exception as e:
    flash(e)
    return render_template('errors/500.html')
  
# posteditvenue
@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    error = False
    body = {}    
    try:    
      name = request.form['name']
      # validate name exist
      existname =  db.session.query(Venue.id).filter(Venue.name==name,Venue.id!=venue_id).first()
      if existname is not None:
        flash("Venue exists.")
        return edit_venue(venue_id)      
      city = request.form['city']
      state = request.form['state']      
      address = request.form['address']
      phone = request.form['phone']
      image_link = request.form['image_link']
      facebook_link = request.form['facebook_link']
      website = request.form['website']
      seeking_talent = request.form.get('seeking_talent')
      print(seeking_talent)
      if(seeking_talent=='y'):
        seeking_talent = True
      else: 
        seeking_talent = False
      print(seeking_talent)
      seeking_description = request.form['seeking_description']
      print(seeking_description)
      genres = request.form.getlist('genres')
      venue = Venue.query.get(venue_id)
      
      venue.name=name
      venue.city=city
      venue.state=state
      venue.address=address
      venue.phone=phone
      venue.image_link=image_link
      venue.facebook_link=facebook_link
      venue.website=website
      venue.seeking_talent=seeking_talent
      venue.seeking_description=seeking_description
      old = db.session.query(Genre.id).join(genres_venue).filter(genres_venue.c.venue_id==venue_id).subquery()
      new_genre_add = db.session.query(Genre).outerjoin(genres_venue).filter(Genre.id.notin_(old),Genre.id.in_(genres)).all()
      existed_genre_delete =  db.session.query(Genre).outerjoin(genres_venue).filter(Genre.id.in_(old),Genre.id.notin_(genres)).all()
      if (new_genre_add is not None):
        for genre in new_genre_add:          
          venue.genres.append(genre)
      if (existed_genre_delete is not None):
        for genre in existed_genre_delete:
          venue.genres.remove(genre)
      print(seeking_description )
      db.session.commit()    
      body['name'] = venue.name      
    except Exception as e:
      error = True
      print(e)
      db.session.rollback()      
    finally:
      db.session.close()
    if not error:
      flash('Venue ' + venue.name + ' was successfully edited!')
      return redirect(url_for('show_venue', venue_id=venue_id))
    else:
      flash('An error occurred. Venue could not be edited.')
      return render_template('errors/500.html')
    return render_template('venues.html')

# deletevenue
@app.route('/venues/<int:venue_id>/delete', methods=['GET','DELETE'])
def delete_venue(venue_id):
  error=''
  try:
    ## check if the value is there
    venue = db.session.query(Venue).filter(Venue.id==venue_id).first()
    if venue.genres is not None:
      venue.genres.clear()
    if venue.artists is not None:
      venue.artists.clear()
    Venue.query.filter_by(id=venue_id).delete()
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if not error:
    flash('Venue' + ' was successfully deleted!')
    return redirect(url_for('venues'))
  else:
    flash('An error occurred. Venue can not be deleted.')
    return render_template('errors/500.html')
  
  return render_template('pages/home.html') 


#  ----------------------------------------------------------------
#  Artist Handlers
#  ----------------------------------------------------------------
# createartist
@app.route('/artists/create',  methods=['GET','POST'])
def create_artist_form():
  form = ArtistForm()
  form.genres.choices = [(genre.id,genre.name) for genre in Genre.query.all()]
  if (request.method == 'POST') : 
    name = form.name.data    
    # check if artist name exist
    existname = Artist.query.filter_by(name=name).first()
    if existname is not None:
      flash("Artist exists.")
      return render_template('forms/new_venue.html', form=form)
    error = False
    body = {}
    try:
      name = request.form.get('name')
      city = request.form.get('city')
      state = request.form.get('state')
      address = request.form.get('address')
      phone = request.form.get('phone')
      image_link = request.form.get('image_link')
      facebook_link = request.form.get('facebook_link')
      website = request.form.get('website')
      
      # SEEKING TALENTS
      seeking_talent = request.form.get('seeking_talent')
      seeking_description = request.form.get('seeking_description')
        
      if(seeking_talent=='y'):
        seeking_talent = True
      else: 
        seeking_talent = False

      genres = request.form.get('genres')

      # CREATE
      artist = Artist(name=name,city=city,state=state,address=address,phone=phone,image_link=image_link,facebook_link=facebook_link,website=website,seeking_talent=seeking_talent,seeking_description=seeking_description)
      
      # GENRE
      genres = request.form.get('genres')
      i=0
      for genre in genres:
        genre = db.session.query(Genre).get(genres[i])
        print(genre)
        artist.genres.extend([genre]) 
        i=i+1 

      db.session.add(artist)
      db.session.commit()
      
      body['name'] = artist.name
    except Exception as e:
      error = True
      print(e)
      db.session.rollback()
    finally:
      db.session.close()
    if not error:
      flash('Artist ' + artist.name + ' was successfully listed!')
      return redirect(url_for('artists'))
    else:
      return render_template('errors/500.html')
  # if request method is GET then generate form
  return render_template('forms/new_venue.html', form=form)

# listartists
@app.route('/artists')
def artists():
  try:        
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
    flash(error)
    return render_template('errors/500.html')

# searchartists
@app.route('/artists/search', methods=['POST'])
def search_artists():
  try:
    search_term=request.form.get('search_term', '')
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

# detailartist
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
      results["seeking_description"]= q.seeking_description
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
      print(results)
    return render_template('pages/show_artist.html', artist = results)
  except Exception as e:
    flash(e)
    return render_template('errors/500.html')

# geteditartist
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  try:
    print(artist_id)
    results= {}
    q=db.session.query(Artist).filter(Artist.id==artist_id).first()
    if(q is None):
      return render_template('errors/404.html')
    else :
      results["id"]= q.id   
      results["name"]= q.name
      results["address"]=q.address
      results["city"]= q.city
      results["state"]= q.state
      results["phone"]= q.phone
      results["website"]= q.website
      results["facebook_link"]= q.facebook_link
      results["seeking_venue"]= q.seeking_venue
      results["seeking_description"]=q.seeking_description
      results["image_link"]= q.image_link
      
      # populate form with existed data
      form = ArtistForm(data=results)
      form.genres.choices = [(genre.id,genre.name) for genre in Genre.query.all()]
      v=[]
      for g in q.genres:
        v.append(str(g.id))
      genres_populate = v
      print(genres_populate)
      form.genres.data = genres_populate 
    return render_template('forms/edit_artist.html', form=form, artist=results)
  except Exception as e:
    flash(e)
    return render_template('errors/500.html')
  
# posteditartist
@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  print('===========')
  error = False
  body = {}    
  try:      
    name = request.form.get('name')
    # validate name exist
    existname =  db.session.query(Artist.id).filter(Artist.name=='artist1',Artist.id!=1).first()
    if existname is not None:
      flash("Artist exists.")
      return edit_artist(artist_id)      
    city = request.form.get('city')
    state = request.form.get('state')      
    address = request.form.get('address')
    phone = request.form.get('phone')
    image_link = request.form.get('image_link')
    facebook_link = request.form.get('facebook_link')
    website = request.form.get('website')
    seeking_venue = request.form.get('seeking_venue')
    print(seeking_venue)
    if(seeking_venue=='y'):
      seeking_venue = True
    else: 
      seeking_venue = False
    print(seeking_venue)
    seeking_description = request.form.get('seeking_description')
    print(seeking_description)
    genres = request.form.getlist('genres')
    artist = Artist.query.get(artist_id)
    
    artist.name=name
    artist.city=city
    artist.state=state
    artist.address=address
    artist.phone=phone
    artist.image_link=image_link
    artist.facebook_link=facebook_link
    artist.website=website
    artist.seeking_venue=seeking_venue
    artist.seeking_description=seeking_description
    old = db.session.query(Genre.id).join(genres_artist).filter(genres_artist.c.artist_id==artist_id).subquery()
    new_genre_add = db.session.query(Genre).outerjoin(genres_artist).filter(Genre.id.notin_(old),Genre.id.in_(genres)).all()
    existed_genre_delete =  db.session.query(Genre).outerjoin(genres_artist).filter(Genre.id.in_(old),Genre.id.notin_(genres)).all()
    if (new_genre_add is not None):
      for genre in new_genre_add:          
        artist.genres.append(genre)
    if (existed_genre_delete is not None):
      for genre in existed_genre_delete:
        artist.genres.remove(genre)
    print(seeking_description )
    db.session.commit()    
    body['name'] = artist.name      
  except Exception as e:
    error = True
    print(e)
    db.session.rollback()      
  finally:
    db.session.close()
  if not error:
    flash('Artist ' + artist.name + ' was successfully edited!')
    return redirect(url_for('show_artist', artist_id=artist_id))
  else:
    flash('An error occurred. Artist could not be edited.')
    return render_template('errors/500.html')
  return render_template('artists.html')

# deleteartist
@app.route('/artists/<int:artist_id>/delete', methods=['GET','DELETE'])
def delete_artist(artist_id):
  error=''
  try:
    ## check if the value is there
    artist = db.session.query(Artist).filter(Artist.id==artist_id).first()
    if artist.genres is not None:
      artist.genres.clear()
    if artist.artists is not None:
      artist.artists.clear()
    Artist.query.filter_by(id=artist_id).delete()
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if not error:
    flash('Artist' + ' was successfully deleted!')
    return redirect(url_for('artists'))
  else:
    flash('An error occurred. Artist can not be deleted.')
    return render_template('errors/500.html')
  
  return render_template('pages/home.html')  

#  ----------------------------------------------------------------  
#  Shows
#  ----------------------------------------------------------------
# listshows
@app.route('/shows')
def shows():
  try:
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

# createshow
@app.route('/shows/create', methods=['GET','POST'])
def create_shows():
  form = ShowForm()
  if (request.method == 'POST') : 
    # check if artist, venue, artistxvenuxstart_time exist
    artist_id = form.artist_id.data  
    existartist = Artist.query.filter_by(id=artist_id).first()
    if existartist is None:
      flash("Artist not exists.")
      return render_template('forms/new_show.html', form=form)
    
    venue_id = form.venue_id.data  
    existvenue = Venue.query.filter_by(id=venue_id).first()
    if existvenue is None:
      flash("Venue not exists.")
      return render_template('forms/new_show.html', form=form)

    start_time = form.start_time.data
    print(start_time)
    existshow = Show.query.filter_by(venue_id=venue_id,artist_id=artist_id,start_time=start_time).first()
    if existshow is not None:
      flash("Show exists.")
      return render_template('forms/new_show.html', form=form)
    error = False
    body = {}
    try:
      artist_id = request.form.get('artist_id')
      venue_id = request.form.get('venue_id')
      start_time = request.form.get('start_time')
      print(start_time)
      show = Show(artist_id=artist_id,venue_id=venue_id,start_time=start_time)
      db.session.add(show)
      db.session.commit()
      
    except Exception as e:
      error = True
      print(e)
      db.session.rollback()
    finally:
      db.session.close()
    if not error:
      flash('Show '  + ' was successfully listed!')
      return redirect(url_for('shows'))
    else:
      flash('An error occurred. Show could not be listed.')
      return render_template('errors/500.html')
  # if request method is GET then generate form
  return render_template('forms/new_show.html', form=form)

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
