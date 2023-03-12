from functools import wraps
from flask import g, redirect, url_for, flash, session

# Current user key in session
CURR_USER_KEY = "curr_user"


class Login(object):
    """Login Class"""

    def do_login(user):
        """Login user."""

        session[CURR_USER_KEY] = user.id

    def do_logout():
        """Logout user."""

        if CURR_USER_KEY in session:
            del session[CURR_USER_KEY]

    def require_login(f):
        """Decorator function to check for Login before route"""
        
        @wraps(f)
        def wrap(*args, **kwargs):
            if g.user:
                if "user_id" in kwargs:
                    kwargs["user_id"] = g.user.id
                return f(*args, **kwargs)
            else:
                flash("You do not have permission to view this page.", "danger")
                return redirect(url_for("auth.login"))
        return wrap
