from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp


class SignupForm(FlaskForm):
    """Add user form"""

    username = StringField("Username",
                           validators=[
                               DataRequired(
                                   message="Username cannot be blank"),
                               Length(min=4, max=50,
                                      message="Username must be between 4 and 50 characters"),
                               Regexp("^[a-zA-Z]+[a-zA-Z0-9]*$",
                                      message="Username can only include letters and numbers and must start with a letter")])

    first_name = StringField("First Name",
                             validators=[
                                 DataRequired(
                                     message="First Name cannot be blank"),
                                 Length(max=50, message="First Name cannot be more than 50 characters")])

    last_name = StringField("Last Name",
                            validators=[
                                DataRequired(
                                    message="Last Name cannot be blank"),
                                Length(max=50, message="Last Name cannot be more than 50 characters")])

    email = EmailField("Email",
                       validators=[
                           DataRequired(message="Email cannot be blank"),
                           Email(message="Please provide a valid email address"),
                           Length(max=50)])

    password = PasswordField("Password",
                             validators=[
                                 DataRequired(
                                     message="Password cannot be blank"),
                                 Length(min=6, max=50, message="Password must be between 6 and 50 characters")])


class UserLoginForm(FlaskForm):
    """User login form"""

    username = StringField("Username",
                           validators=[
                               DataRequired(
                                   message="Username cannot be blank"),
                               Length(min=4, max=50,
                                      message="Username must be between 4 and 50 characters"),
                               Regexp("^[a-zA-Z]+[a-zA-Z0-9]*$",
                                      message="Username can only include letters and numbers and must start with a letter")])

    password = PasswordField("Password",
                             validators=[
                                 DataRequired(
                                     message="Password cannot be blank"),
                                 Length(min=6, max=50, message="Password must be between 6 and 50 characters")])


class UserEditForm(FlaskForm):
    """User profile edit form"""

    username = StringField("Username",
                           validators=[
                               DataRequired(), Length(max=50)])

    first_name = StringField("First Name",
                             validators=[
                                 DataRequired(
                                     message="First name is required."),
                                 Length(max=50, message="First name cannot be more than 50 characters")])

    last_name = StringField("Last Name",
                            validators=[
                                DataRequired(message="Last name is required."),
                                Length(max=50, message="Last name cannot be more than 50 characters")])

    email = EmailField("Email",
                       validators=[
                           DataRequired(message="Email is required."),
                           Email(message="Email address is not valid."),
                           Length(max=50, message="Email cannot be more than 50 characters")])


class ChangePasswordForm(FlaskForm):
    """User change password form"""
    current_password = PasswordField("Current Password",
                                     validators=[
                                         DataRequired(
                                             message="Current password cannot be blank."),
                                         Length(min=6, max=50, message="Password must be between 6 and 50 characters")])

    new_password = PasswordField("New Password",
                                 validators=[
                                     DataRequired(
                                         message="Password cannot be blank."),
                                     Length(min=6, max=50, message="Password must be between 6 and 50 characters")])

    new_password_retype = PasswordField("Confirm Password",
                                        validators=[
                                            DataRequired(
                                                message="Password cannot be blank."),
                                            Length(
                                                min=6, max=50, message="Password must be between 6 and 50 characters"),
                                            EqualTo("new_password",
                                                    message="Passwords don't match.")])
