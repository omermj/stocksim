from flask import render_template, flash, redirect, g, url_for, Blueprint
from sqlalchemy.exc import IntegrityError
from users.models import User
from auth.forms import SignupForm, UserLoginForm
from auth.login import Login, CURR_USER_KEY


class Operations(object):
    """Class for Authentication Operations"""

    @classmethod
    def handle_signup(cls):
        """Show signup form and process form on submission"""

        # If a user is already logged in, show User Dashboard
        if g.user:
            return redirect(url_for("users.show_user_dashboard", user_id=g.user.id))

        # Render signup form
        form = SignupForm()

        # If form is submitted, validate data
        if form.validate_on_submit():

            # Create user in db
            user = User.signup(username=form.username.data,
                               email=form.email.data,
                               first_name=form.first_name.data,
                               last_name=form.last_name.data,
                               password=form.password.data)

            # If there is an error
            if not isinstance(user, User):
                flash(user["error"], "danger")
                return render_template("signup.html", form=form)

            # Login user
            Login.do_login(user)
            flash("Thank you for signing up to StockSim. Happy Trading!.", "success")
            return redirect(url_for("users.show_user_dashboard", user_id=user.id))

        return render_template("signup.html", form=form)

    @classmethod
    def handle_login(cls):
        """Show login form and login user on validation"""

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

    @classmethod
    def handle_logout(cls):
        """Logout user"""

        # Check if a there is a logged in user
        if g.user:
            Login.do_logout()
            flash("You have been logged out.", "secondary")

        return redirect(url_for("show_homepage"))
