from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField, HiddenField
from wtforms.validators import DataRequired

class AddAnimalForm(FlaskForm):
    id = HiddenField('id')
    name = StringField('Name', validators=[DataRequired()])
    type = StringField('Type', validators=[DataRequired()])
    description = TextField('Description', validators=[DataRequired()])
    image_url = StringField('Image URL', validators=[DataRequired()])
    submit = SubmitField('Add Animal')
