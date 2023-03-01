from flask import redirect, render_template, flash, Blueprint, url_for, g, request
from watchlists.models import db, Watchlist
from watchlists.forms import CreateWatchlistForm
from auth.login import Login


watchlists = Blueprint("watchlists", __name__, template_folder="templates")


@watchlists.route("/", methods=["GET", "POST"])
@Login.require_login
def watchlist_home():
    """Show all watchlists"""

    form = CreateWatchlistForm()



    if form.validate_on_submit():
        watchlist = Watchlist.create(name=form.name.data,
                                     description=form.description.data,
                                     user_id=g.user.id)
        if watchlist:
            flash("New watchlist is successfully created.", "success")
        else:
            flash("Error creating watchlist.", "danger")
        return redirect(url_for("watchlists.watchlist_home"))

    return render_template("watchlists.html", watchlists=g.user.watchlists,
                           form=form)


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
def create_watchlist():
    """Create a new watchlist"""

    symbol = request.form
    print(symbol)
    return redirect("/")
