from flask_wtf import FlaskForm
from wtforms import PasswordField, EmailField, SubmitField, StringField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
    title = StringField('Post Title', validators=[DataRequired()])
    content = StringField('Post Description', validators=[DataRequired()])
    submit = SubmitField('Create Post')