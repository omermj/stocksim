# import re
# from sqlalchemy.exc import IntegrityError
# from users.models import User
# from flask import render_template, flash, redirect, url_for
# from auth.login import Login


# class Signup(object):
#     """Sign Class"""

#     @classmethod
#     def create_user_in_db(cls, form):
#         """Create user in db from sign up form data"""

#         try:
#             user = User.signup(username=form.username.data,
#                                email=form.email.data,
#                                first_name=form.first_name.data,
#                                last_name=form.last_name.data,
#                                password=form.password.data)
#         except IntegrityError:
#             return {"error": "Username already taken"}
#         except:
#             return {"error": "An error occured while creating the account."}
#         else:
#             Login.do_login(user)
#             return user

    # def validate_signup_form(form_data):
    #     """Validate signup form data
    #     Returns True if validation is successful,
    #     else return {"errors": {"field": "message"}}"""

    #     # Username Validation (Between 4 to 50 characters, can only include
    #     # letters and numbers and must start with letter)
    #     if not Signup.validate_username(form_data.username):

    # @classmethod
    # def validate_username(cls, username):
    #     """Validate username. Returns True if validated,
    #     else return {"username": "error message"}"""

    #     # Check length
    #     if len(username) < 4 or len(username) > 50:
    #         return {"username": "Username must be between 4 and 50 characters"}

    #     # Check for pattern (start with letter, can only include letters and numbers)
    #     pattern = re.compile(r"^[a-zA-Z]+[a-zA-Z0-9]*$")
    #     if not re.fullmatch(pattern, username):
    #         return {"username":
    #                 "Username can only include letters and numbers and must start with a letter"}

    #     # Check if username already exists in db
    #     if User.query.filter(User.username == username).first():
    #         return {"username": "Username is already taken"}

    #     return True

    # @classmethod
    # def validate_name(cls, name):
    #     """Validate name. Returns True if validated
    #     else return {"name": "error message"}"""

    #     # Check length
    #     if len(name) < 4 or len(name) > 50:
    #         return {"name": "Name must be between 4 and 50 characters"}

    #     return True

    # @classmethod
    # def validate_email(cls, email):
    #     """Validate name. Returns True if validated
    #     else return {"name": "error message"}"""

    #     # Check length
    #     if len(email) < 4 or len(email) > 50:
    #         return {"email": "Email must be between 4 and 50 characters"}

    #     # Check for regex pattern
    #     pattern = re.compile(r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$")
    #     if not re.fullmatch(pattern, email):
    #         return {"email":
    #                 "Email address is not valid"}

    #     return True

    # @classmethod
    # def validate_password(cls, password):
    #     """Validate password. Returns True if validated
    #     else return {"name": "error message"}"""

    #     # Check length
    #     if len(password) < 6 or len(password) > 60:
    #         return {"password": "Password must be between 6 and 50 characters"}

    #     return True
