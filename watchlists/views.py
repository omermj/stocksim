from flask import redirect, render_template, flash, Blueprint, url_for, g, request, jsonify
from watchlists.models import Watchlist
from stocks.models import Stock
from watchlists.forms import WatchlistForm
from auth.login import Login


class Views(object):
    """View functions for Watchlists"""

    @classmethod
    def show_watchlist_home(cls):
        """Show the homepage for watchlists"""

        form = WatchlistForm()
        return render_template("watchlists.html", watchlists=g.user.watchlists,
                               form=form)

    

    @classmethod
    def show_watchlist(cls, watchlist_id):
        """Show watchlist with stocks"""

        watchlist = Watchlist.query.get(watchlist_id)
        form = WatchlistForm(obj=watchlist)

        return render_template("watchlist_details.html",
                               watchlist=watchlist, form=form)
    
    
