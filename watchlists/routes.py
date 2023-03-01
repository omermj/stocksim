from flask import redirect, render_template, flash, Blueprint, url_for, g, request
from watchlists.models import db, Watchlist
from auth.login import Login

watchlists = Blueprint("watchlists", __name__, template_folder="templates")


@watchlists.route("/")
@Login.require_login
def watchlist_home():
    """Show all watchlists"""

    # watchlists = Watchlist.query.filter(Watchlist.user_id == g.user.id)

    return render_template("watchlists.html", watchlists=g.user.watchlists)


@watchlists.route("/<int:watchlist_id>")
@Login.require_login
def show_watchlist(watchlist_id):
    """Show details page for watchlist"""

    # Get the watchlist
    watchlist = Watchlist.query.get(watchlist_id)

    return render_template("watchlist_details.html",
                           watchlist=watchlist, stocks=watchlist.get_all_stocks())

@watchlists.route("/", methods=["POST"])
@Login.require_login
def add_stock_to_watchlist():
    """Add stock to watchlist"""

    symbol = request.form
    print(symbol)
    return redirect("/")