from flask import redirect, render_template, flash, Blueprint, url_for, g
from watchlists.models import db, Watchlist
from auth.login import Login

watchlists = Blueprint("watchlists", __name__, template_folder="templates")


@watchlists.route("/")
@Login.require_login
def watchlist_home():
    """Show all watchlists"""

    # watchlists = Watchlist.query.filter(Watchlist.user_id == g.user.id)
    
    return render_template("watchlists.html", watchlists=g.user.watchlists)



