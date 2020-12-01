from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class TagForm(FlaskForm):
    value=StringField('Value', validators=[DataRequired()])
    submit=SubmitField('Submit')