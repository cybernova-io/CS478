from flask_wtf import FlaskForm
from wtforms import PasswordField, EmailField, SubmitField, StringField, DateField
from wtforms.validators import DataRequired

class SignupForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    major = StringField('Major', validators=[DataRequired()])
    grad_year = DateField('Graduation Year', format='%Y', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')