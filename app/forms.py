from flask_wtf import FlaskForm, Form
from flask_wtf.file import FileField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember Me')
	submit = SubmitField('Sign In')

class UploadForm(FlaskForm):
    availability = IntegerField ('Minutes available', validators=[DataRequired()])
    datafile = FileField('Upload File', validators=[DataRequired()])
    submit = SubmitField('Upload')
