from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length


class WatchlistForm(FlaskForm):
    """Form for placing a new trade"""

    name = StringField("Name",
                       validators=[
                           DataRequired(
                               message="Name is required"),
                           Length(2, 20,
                                  message="Name must be between 2 and 20 characters")])

    description = StringField("Description",
                              validators=[
                                  Length(
                                      max=50,
                                      message="Description cannot exceed 50 characters.")])
