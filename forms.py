import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField,BooleanField,SubmitField,IntegerField
from wtforms.validators import AnyOf, DataRequired, Length, NumberRange, Regexp, URL, ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask_sqlalchemy import SQLAlchemy
from wtforms.fields.html5 import TelField
from wtforms.widgets.html5 import NumberInput, TelInput
from flask_wtf.recaptcha import widgets

class ShowForm(FlaskForm):
    artist_id = IntegerField(
        'artist_id',widget=NumberInput(min=1),validators=[DataRequired()]
    )
    venue_id = IntegerField(
        'venue_id',widget=NumberInput(min=1),validators=[DataRequired()]    
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired(),Regexp('(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})')],
        default= datetime.datetime.now(),
        # render_kw={'disabled':''}
    )    
    submit = SubmitField('Save')

class VenueForm(FlaskForm):
    
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=[
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    phone = IntegerField(
        'phone',widget=NumberInput(min=1000000000,max=9999999999), validators=[DataRequired(),NumberRange(min=10,max=10,message="Only 10-number phone")]
    )
    image_link = StringField(
        'image_link', validators=[URL()]
    )
    genres = SelectMultipleField('genres',choices=[], validators=[DataRequired()])
    seeking_talent = BooleanField('seeking_talent', default='checked',false_values=(False, 'false', '',))
    seeking_description = StringField(
        'seeking_description'
    )
    website = StringField(
        'website', validators=[URL()]
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL()]
    )
    submit = SubmitField('Save')    

    

class ArtistForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=[
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]
    )
    phone = IntegerField(
        'phone',widget=NumberInput(min=1000000000,max=9999999999), validators=[DataRequired(),NumberRange(min=10,max=10)]
    )
    image_link = StringField(
        'image_link',validators=[URL()]
    )
    seeking_venue = BooleanField('seeking_talent', default='checked',false_values=(False, 'false', '',))
    seeking_description = StringField(
        'seeking_description'
    )
    #dynamic choices 
    genres = SelectMultipleField('genres',choices=[],validators=[DataRequired()])
    website = StringField(
        'website', validators=[URL()]
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL()]
    )    
    submit = SubmitField('Save')

