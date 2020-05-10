Fyyur
-----

### Introduction

Fyyur is a musical venue and artist booking site that facilitates the discovery and bookings of shows between local performing artists and venues. This site lets you list new artists and venues, discover them, and list shows with artists as a venue owner.

### Tech Stack

Our tech stack will include:

* **SQLAlchemy ORM** to be our ORM library of choice
* **PostgreSQL** as our database of choice
* **Python3** and **Flask** as our server language and server framework
* **Flask-Migrate** for creating and running schema migrations
* **HTML**, **CSS**, and **Javascript** with [Bootstrap 3](https://getbootstrap.com/docs/3.4/customize/) for our website's frontend

### Main Files: Project Structure

  ```sh
  ├── README.md
  ├── app.py *** the main driver of the app. Includes your SQLAlchemy models.
                    "python app.py" to run after installing dependences
  ├── config.py *** Database URLs, CSRF generation, etc
  ├── error.log
  ├── forms.py *** Your forms
  ├── requirements.txt *** The dependencies we need to install with "pip3 install -r requirements.txt"
  ├── static
  │   ├── css 
  │   ├── font
  │   ├── ico
  │   ├── img
  │   └── js
  └── templates
      ├── errors
      ├── forms
      ├── layouts
      └── pages
  ```

### ENVIRONMENT AND MIGRATE
//////////////////////SET UP ENV
cd YOUR_PROJECT_DIRECTORY_PATH/
py -m venv env
.\env\scripts\activate

pip install -r requirements.txt

//////////////////////SET UP DATABASE

flask db init
flask db migrate
flask db upgrade

********** database sample datas are available under sql_sample.data.txt

//////////////////////RUN
set flask_app=app
set flask_debug=on
set flask_env=development
flask run

########### Error
'function' has no attribute 'c'
	- Use a proper class instead of an association table.
	- Check carefully the relationship (use "table_name" not class_name), backref

No system function found '<class function>':
	- from sqlalchemy import func	 =>>>>> Use: fun.count() 
	- If you use a correct table name (Visual Studio code does not prompt error if you use a duplicate word even if it's commented out)
	
datetime is not JSON serializable ( when passing datetime data from database):
	-when render template at the end : venue=json.dumps(results, indent=4, sort_keys=True, default=str)

Check if query return empty:
	- use first() instead of one()
	- if (query is None): ....
	
	
javascript not take action / no render :
	$("#createVenue").on("click", function(e) {
		//document.getElementById('create-venue-form').onsubmit = function(e) {
		e.preventDefault(); ....
		
datetime.datetime cannot be passed 
	variable_to_pass = str(query.result)
	
Form and App different / circular import / Query choices
	In forms.py: class VenueForm(): seeking_venue = BooleanField('seeking_talent', default='checked',false_values=(False, 'false', '',))
	In app.py where call VenueForm(): form.genres.choices = [(genre.id,genre.name) for genre in Genre.query.all()]
	
Datetime picker
	https://www.solodev.com/blog/web-design/adding-a-datetime-picker-to-your-forms.stml
		(place the bootstap picker after jquery)
	download two files .woff and .woff2 at https://github.com/twbs/bootstrap-sass/tree/master/assets/fonts/bootstrap
	place the script right in the page between <script> tag, instead of a separate file
	format and hide the AM/PM toggle
		$(function() {
            $('#datetimepicker1').datetimepicker({
                format: 'YYYY-MM-DD hh:mm:ss'
            }).on('dp.show', function(event) {
                $(".bootstrap-datetimepicker-widget").find('.btn[data-action="togglePeriod"]').hide();
            });
        });
	
BooleanField:
	value ='y' is checked else None => request.form.get('booleanfield')
	
	request.form['booleanfield'] only if you know the field exists or else error
	
IntegerField:
	validator is NUMBERRANGE not LENGTH. It will fail instead of prompt message (if use wrong validators)
	
	
You can add a validators inside FlaskForm
	But in your app.py, we need to use form.validate() or .validate_on_submit()