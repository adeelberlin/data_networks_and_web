from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, HiddenField
from wtforms.validators import DataRequired

class VoteForm(FlaskForm):
    id = HiddenField('id')
    votes = IntegerField('Votes',default=0, validators=[DataRequired()])
    submit = SubmitField('Vote')
