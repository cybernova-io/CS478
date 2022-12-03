from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, TextAreaField, DateField, TimeField
from wtforms.validators import DataRequired

class EventForm(FlaskForm):
    name = StringField('Event Name', validators=[DataRequired()])
    description = TextAreaField('Event Description', validators=[DataRequired()])
    date = DateField('Event Date', validators=[DataRequired()])
    time = TimeField('Event Time', validators=[DataRequired()])
    submit = SubmitField('Create Event')