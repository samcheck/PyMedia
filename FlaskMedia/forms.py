from flask_wtf import FlaskForm as Form
from wtforms import StringField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length

class EditMovieForm(Form):
    title = StringField('title', validators=[DataRequired()])
    plot = TextAreaField('plot', validators=[Length(min=0, max=2047)])
