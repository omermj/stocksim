from flask import Blueprint
from auth.login import Login
from auth.operations import Operations


auth = Blueprint("auth", __name__, template_folder="templates")
operations = Operations()


@auth.route("/signup", methods=["POST", "GET"])
def signup():
    """Handle user signup.

    Create new user in db, logins in user and redirect to user homepage"""

    return operations.handle_signup()


@auth.route("/login", methods=["POST", "GET"])
def login():
    """Login user and display user dashboard"""

    return operations.handle_login()


@auth.route("/logout")
@Login.require_login
def logout():
    """Logout user"""

    return operations.handle_logout()
