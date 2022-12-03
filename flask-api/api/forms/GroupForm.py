from flask_wtf import FlaskForm
from wtforms import PasswordField, EmailField, SubmitField, StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired

class GroupForm(FlaskForm):
    name = StringField('Group Name', validators=[DataRequired()])
    description = TextAreaField('Group Description', validators=[DataRequired()])
    inviteOnly = SelectField('Group Is Invite Only', choices=("No", "Yes"), validators=[DataRequired()])
    submit = SubmitField('Create Group')