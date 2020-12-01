from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectMultipleField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title=StringField('Title', validators=[DataRequired()])
    tags=SelectMultipleField('Tags', coerce=int,validate_choice=False, choices=[])
    content=TextAreaField('Content', validators=[DataRequired()])
    submit=SubmitField('Submit')