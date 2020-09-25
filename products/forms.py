from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp

photos = UploadSet('photos',IMAGES)

class CreateItem(FlaskForm):
	title = StringField('Title',[DataRequired(),Regexp('^\w+$',message="Name must contain only letters")])
	price = StringField('Price',[DataRequired(),Regexp('^\d*.?\d$',message="Name must contain only numbers")])
	description = StringField('Description',[DataRequired(),Length(min=8)])
	submit  = SubmitField('Submit')

class EditItem(FlaskForm):
	title = StringField('Title',[DataRequired(),Regexp('^\w+$',message="Name must contain only letters")])
	price = StringField('Price',[DataRequired(),Regexp('^\d*.?\d$',message="Name must contain only numbers")])
	description = StringField('Description',[DataRequired(),Length(min=8)])
	submit  = SubmitField('Submit')

