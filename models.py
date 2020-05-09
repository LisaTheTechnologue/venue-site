import datetime
import app 
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)
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

# class Shows(object):
#     """
#     Shows object the "shows" table.
#     """
#     def __init__(self, venue_id, artist_id):
#         self.venue_id = venue_id
#         self.artist_id = artist_id

# shows = db.Table("shows",
#         db.metadata,
#         db.Column("id", db.Integer, primary_key = True),
#         db.Column("venue_id", db.Integer, db.ForeignKey("venue.id")),
#         db.Column("artist_id", db.Integer, db.ForeignKey("artist.id")),
#         db.Column("start_time",db.DateTime, nullable=True, default=func.now())
#         )

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
    address = db.Column(db.String())
    phone = db.Column(db.String(10))
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



db.mapper(Genres_venue, genres_venue)
db.mapper(Genres_artist, genres_artist)
# db.mapper(Shows, shows)