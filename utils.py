from flask import Flask, redirect, render_template, session, g, url_for
from users.models import User
from auth.login import CURR_USER_KEY


def add_user_to_session():
    """If logged in, add user to Flask global (g)"""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None

def homepage_view():
    """Show home page view depending on user login status"""

    # If user is logged in, show dashboard, else show homepage
    if g.user:
        return redirect(url_for("users.show_user_dashboard", user_id=g.user.id))

    return render_template("homepage.html")

def request_header(req):
    """Add request header before every request"""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req