from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import DataRequired, Email, Length


class UserAddForm(FlaskForm):
    """Add user form"""

    username = StringField("Username", validators=[
                           DataRequired(), Length(max=50)])
    first_name = StringField("First Name", validators=[
                             DataRequired(), Length(max=50)])
    last_name = StringField("Last Name", validators=[
                            DataRequired(), Length(max=50)])
    email = EmailField("Email", validators=[DataRequired(), Email(),
                                            Length(max=50)])
    password = PasswordField("Password", validators=[
                             DataRequired(), Length(min=6, max=50)])


class UserLoginForm(FlaskForm):
    """User login form"""

    username = StringField("Username", validators=[
                           DataRequired(), Length(max=50)])
    password = PasswordField("Password", validators=[
                             DataRequired(), Length(min=6, max=50)])