from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, RadioField, IntegerField
from wtforms.validators import DataRequired, Email, Length


class CreateWatchlistForm(FlaskForm):
    """Form for placing a new trade"""

    name = StringField("Name", validators=[DataRequired(), Length(2, 20)])
    description = StringField("Description", validators=[Length(max=50)])
