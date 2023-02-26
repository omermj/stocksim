from flask import render_template, flash, redirect, session, g, url_for, Blueprint
from sqlalchemy.exc import IntegrityError
from users.models import User
from auth.forms import UserAddForm, UserLoginForm
from db import db
from auth.login import Login, CURR_USER_KEY


auth = Blueprint("auth", __name__, template_folder="templates")


# def do_login(user):
#     """Login user."""

#     session[CURR_USER_KEY] = user.id


# def do_logout():
#     """Logout user."""

#     if CURR_USER_KEY in session:
#         del session[CURR_USER_KEY]


@auth.route("/signup", methods=["POST", "GET"])
def signup():
    """Handle user signup.

    Create new user in db, logins in user and redirect to user homepage"""

    # If a user is already logged in, show User Dashboard
    if g.user:
        return redirect(url_for("users.show_user_dashboard", user_id=g.user.id))

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(username=form.username.data,
                               email=form.email.data,
                               first_name=form.first_name.data,
                               last_name=form.last_name.data,
                               password=form.password.data)
        except IntegrityError:
            flash("Username already taken.", "danger")
            return render_template("signup.html", form=form)
        else:
            Login.do_login(user)
            flash("Thank you for signing up to StockSim. Happy Trading!.", "success")
            return redirect(url_for("users.show_user_dashboard", user_id=user.id))
    else:
        return render_template("signup.html", form=form)


@auth.route("/login", methods=["POST", "GET"])
def login():
    """Login user and display user dashboard"""

    # If a user is already logged in, show User Dashboard
    if g.user:
        return redirect(url_for("users.show_user_dashboard", user_id=g.user.id))

    form = UserLoginForm()

    if form.validate_on_submit():
        user = User.authenticate(username=form.username.data,
                                 password=form.password.data)

        if user:
            Login.do_login(user)
            flash(
                f"Login successful. Welcome back {user.username}.", "success")
            return redirect(url_for("users.show_user_dashboard", user_id=user.id))
        else:
            flash("Username/Password is invalid.", "danger")

    return render_template("login.html", form=form)


@auth.route("/logout")
def logout():
    """Log out user."""

    # Check if a there is a logged in user
    if g.user:
        Login.do_logout()
        flash("You have been logged out.", "secondary")

    return redirect(url_for("show_homepage"))
