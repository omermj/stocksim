from flask import redirect, render_template, flash, url_for, g, jsonify
from watchlists.models import Watchlist
from stocks.models import Stock
from watchlists.forms import WatchlistForm


class Operations(object):
    """Operation functions for Watchlists"""

    @classmethod
    def add_watchlist(cls):
        """Add new watchlist on form submission"""

        form = WatchlistForm()

        # If form is validated, add watchlist
        if form.validate_on_submit():
            watchlist = Watchlist.create(name=form.name.data,
                                         description=form.description.data,
                                         user_id=g.user.id)
            if watchlist:
                flash("New watchlist is successfully created.", "success")
                return redirect(url_for("watchlists.watchlist_home"))
            else:
                flash("Error creating watchlist. Please try again.", "danger")

        return render_template("watchlists.html", watchlists=g.user.watchlists,
                               form=form)

    @classmethod
    def edit_watchlist(cls, watchlist_id):
        """Edit watchlist"""

        watchlist = Watchlist.query.get(watchlist_id)
        form = WatchlistForm(obj=watchlist)

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
                               watchlist=watchlist, form=form)

    @classmethod
    def remove_watchlist(cls, watchlist_id):
        """Remove watchlist."""

        watchlist = Watchlist.query.get(watchlist_id)

        if Watchlist.remove(watchlist):
            return jsonify({"result": "success"})
        else:
            return jsonify({"result": "error"})

    @classmethod
    def add_stock(cls, watchlist_id, request):
        """Add stock to watchlist ID"""

        # Get stock symbol and watchlist
        watchlist = Watchlist.query.get(watchlist_id)
        symbol = request.json["symbol"]

        # Add stock symbol to watchlist and return results
        response = watchlist.add_stock(symbol=symbol)

        return jsonify(response)

    @classmethod
    def remove_stock(cls, watchlist_id, stock_id):
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
