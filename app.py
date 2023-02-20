from flask import Flask, redirect
from flask_debugtoolbar import DebugToolbarExtension
from config import Config
from db import db, connect_db
from users.models import User
from trades.models import Trade
from watchlists.models import Watchlist
from stocks.models import Stock, Watchlist_Stock
from users.routes import users
from trades.routes import trades
from watchlists.routes import watchlists




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


# Root view
@app.route("/")
def root():
    """Homepage: redirect to /playlists."""

    return "connected"
