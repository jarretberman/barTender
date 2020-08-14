from flask_wtf import FlaskForm
from wtforms import TextAreaField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    """Form for adding posts."""

    content = TextAreaField('What did you make today?', validators=[DataRequired()])

class CommentForm(FlaskForm):
    """Form for adding comments."""

    content = TextAreaField('', validators=[DataRequired()])