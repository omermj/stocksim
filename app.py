from flask import Flask, redirect, render_template, session, g, url_for
from flask_debugtoolbar import DebugToolbarExtension
from config import Config
from db import db, connect_db
from users.models import User
from users.routes import users
from trades.routes import trades
from watchlists.routes import watchlists
from auth.routes import auth

from auth.login import CURR_USER_KEY

# Create Flask App
app = Flask(__name__)
app.config.from_object(Config)

# Connect to database
connect_db(app)
db.create_all()

# Enable DTE
debug = DebugToolbarExtension(app)


# Blueprints
app.register_blueprint(users, url_prefix="/users")
app.register_blueprint(trades, url_prefix="/trades")
app.register_blueprint(watchlists, url_prefix="/watchlists")
app.register_blueprint(auth, url_prefix="/auth")


# Run before each request
@app.before_request
def add_user_to_g():
    """If logged in, add user to Flask global (g)"""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None


# Root view
@app.route("/")
def show_homepage():
    """Homepage: redirect to /playlists."""

    # If user is logged in, show dashboard, else show homepage
    if g.user:
        return redirect(url_for("users.show_user_dashboard", user_id=g.user.id))

    return render_template("homepage.html")


@app.after_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req


@app.errorhandler(404)
def page_not_found(e):
    """404 page"""

    return render_template("404.html"), 404