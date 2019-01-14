from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField,SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from wtforms.widgets import TextArea
from app.models import User


class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators =[DataRequired()])
	submit = SubmitField('Sign In')

class AddBookForm(FlaskForm):
	title = StringField('Title', validators=[DataRequired()])
	author = StringField('Author', validators=[DataRequired()])
	description = StringField('Description', widget=TextArea(), validators=[DataRequired()])
	pages = IntegerField('Pages', validators=[DataRequired()])
	submit = SubmitField('Add')


class RegistrationForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	password2 = PasswordField(
    	'Repeat Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Register')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user is not None:
			raise ValidationError('Please use a different username')


	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is not None:
			raise ValidationError('Please use a different email address')

