from flask import redirect, render_template, flash, Blueprint, url_for, g, request, jsonify
from watchlists.models import Watchlist
from stocks.models import Stock
from watchlists.forms import CreateWatchlistForm
from auth.login import Login


watchlists = Blueprint("watchlists", __name__,
                       template_folder="templates", static_folder="static")


@watchlists.route("/", methods=["GET", "POST"])
@Login.require_login
def watchlist_home():
    """Show all watchlists"""

    # Get create watchlist form
    form = CreateWatchlistForm()

    # If form is submitted, add watchlist
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


@watchlists.route("/<int:watchlist_id>", methods=["GET", "POST"])
@Login.require_login
def show_watchlist(watchlist_id):
    """Show details page for watchlist and edit watchlist if edit request is submitted"""

    # Get the watchlist and watchlist form for editing
    watchlist = Watchlist.query.get(watchlist_id)
    form = CreateWatchlistForm(obj=watchlist)

    # If edit watchlist form is submitted, update watchlist in db
    if form.validate_on_submit():
        response = watchlist.edit(new_name=form.name.data,
                                  new_description=form.description.data)
        if response:
            flash("Watchlist has been successfully edited.", "success")

        else:
            flash("There was an error editing the watchlist. Please try again.",
                  "danger")

    return render_template("watchlist_details.html",
                           watchlist=watchlist,
                           stocks=watchlist.get_all_stocks(),
                           form=form)


@watchlists.route("/<int:watchlist_id>", methods=["DELETE"])
@Login.require_login
def remove_watchlist(watchlist_id):
    """Remove watchlist."""

    watchlist = Watchlist.query.get(watchlist_id)

    if Watchlist.remove(watchlist):
        return jsonify({"result": "success"})
    else:
        return jsonify({"result": "error"})


@watchlists.route("/<int:watchlist_id>/addstock", methods=["POST"])
@Login.require_login
def add_stock_to_watchlist(watchlist_id):
    """Add stock to watchlist ID"""

    # Get stock symbol and watchlist
    watchlist = Watchlist.query.get(watchlist_id)
    symbol = request.json["symbol"]

    # Add stock symbol to watchlist and return results
    response = watchlist.add_stock(symbol=symbol)

    return jsonify(response)


@watchlists.route("/<int:watchlist_id>/removestock/<int:stock_id>", methods=["DELETE"])
@Login.require_login
def remove_stock_from_watchlist(watchlist_id, stock_id):
    """Remove stock from watchlist ID"""

    # Get stock symbol and watchlist
    watchlist = Watchlist.query.get(watchlist_id)
    stock = Stock.query.get(stock_id)

    # Add stock symbol to watchlist and return results
    response = watchlist.remove_stock(symbol=stock.symbol)

    if response:
        return jsonify({"result": "success"})
    else:
        return jsonify({"result": "unsuccessful"})
