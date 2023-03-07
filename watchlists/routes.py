from flask import Blueprint, request
from auth.login import Login
from watchlists.views import Views
from watchlists.operations import Operations


watchlists = Blueprint("watchlists", __name__,
                       template_folder="templates", static_folder="static")
views = Views()
operations = Operations()


@watchlists.route("/")
@Login.require_login
def watchlist_home():
    """Show all watchlists"""

    return views.show_watchlist_home()


@watchlists.route("/", methods=["POST"])
@Login.require_login
def add_watchlist():
    """Add new watchlist"""

    return operations.add_watchlist()


@watchlists.route("/<int:watchlist_id>")
@Login.require_login
def show_watchlist(watchlist_id):
    """Show details page for watchlist"""

    return views.show_watchlist(watchlist_id=watchlist_id)


@watchlists.route("/<int:watchlist_id>", methods=["POST"])
@Login.require_login
def edit_watchlist(watchlist_id):
    """Edit watchlist"""

    return operations.edit_watchlist(watchlist_id=watchlist_id)


@watchlists.route("/<int:watchlist_id>", methods=["DELETE"])
@Login.require_login
def remove_watchlist(watchlist_id):
    """Remove watchlist"""

    return operations.remove_watchlist(watchlist_id=watchlist_id)


@watchlists.route("/<int:watchlist_id>/addstock", methods=["POST"])
@Login.require_login
def add_stock_to_watchlist(watchlist_id):
    """Add stock to watchlist"""

    return operations.add_stock(watchlist_id=watchlist_id, request=request)


@watchlists.route("/<int:watchlist_id>/removestock/<int:stock_id>", methods=["DELETE"])
@Login.require_login
def remove_stock_from_watchlist(watchlist_id, stock_id):
    """Remove stock from watchlist"""

    return operations.remove_stock(watchlist_id=watchlist_id, stock_id=stock_id)
