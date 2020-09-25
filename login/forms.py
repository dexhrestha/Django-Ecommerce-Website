from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField,PasswordField
from wtforms.validators import DataRequired, Length ,Email,Regexp,EqualTo

class SignupForm(FlaskForm):
	fname = StringField('First Name',[DataRequired(),Regexp('^\w+$',message="Name must contain only letters")])
	lname = StringField('Last Name',[DataRequired(),Regexp('^\w+$',message="Name must contain only letters")])
	email = StringField('Email ',[Email(message=('Not a valid email address')),
								DataRequired()])
	password = PasswordField('Password',[DataRequired(),
						Length(min=8,max=32,message=('Your password is too short')),
						EqualTo('confirm',message='Passwords must match')])
	confirm = PasswordField('Re-enter Password')
	submit  = SubmitField('Submit')

class LoginForm(FlaskForm):
	email = StringField('Email ',[Email(message=('Not a valid email address')),
								DataRequired()])
	password = PasswordField('Password',[DataRequired(),
						Length(min=8,max=32,message=('Your password is too short')),
						])
	submit = SubmitField('Login')


class EditInfoForm(FlaskForm):
	fname = StringField('First Name',[DataRequired(),Regexp('^\w+$',message="Name must contain only letters")])
	lname = StringField('Last Name',[DataRequired(),Regexp('^\w+$',message="Name must contain only letters")])
	email = StringField('Email ',[Email(message=('Not a valid email address')),
								DataRequired()])
	submit  = SubmitField('Edit')


class ChangePassword(FlaskForm):
	old_password = PasswordField('Old Password',[DataRequired(),
						Length(min=8,max=32,message=('Your password is too short'))])
	password = PasswordField('Password',[DataRequired(),
						Length(min=8,max=32,message=('Your password is too short')),
						EqualTo('confirm',message='Passwords must match')])
	confirm = PasswordField('Re-enter Password')
	submit  = SubmitField('Change Password')
		
	
	


