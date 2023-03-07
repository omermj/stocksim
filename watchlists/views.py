from flask import render_template, g
from watchlists.models import Watchlist
from watchlists.forms import WatchlistForm


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
