from flask import Blueprint, request
from auth.login import Login
from trades.views import Views
from trades.operations import TradeOperations

trades = Blueprint("trades", __name__,
                   template_folder="templates", static_folder="static")
views = Views()
operations = TradeOperations()


@trades.route("/<int:trade_id>")
@Login.require_login
def show_trade_details(trade_id):
    """Show trade details"""

    return views.show_trade_details(trade_id)


@trades.route("/open")
@Login.require_login
def show_open_positions():
    """Show all open positions for the logged in user"""

    return views.show_open_positions()


@trades.route("/history")
@Login.require_login
def show_trading_history():
    """Show trading history for the logged in user"""

    return views.show_trading_history()


@trades.route("/new")
@Login.require_login
def show_new_trade_form():
    """Show New Trade Form"""

    return views.show_new_trade_form()


@trades.route("/new", methods=["POST"])
@Login.require_login
def enter_new_trade():
    """Enter new trade and return result as JSON"""

    return operations.enter_new_trade(request)


@trades.route("/<int:trade_id>/close", methods=["PUT"])
@Login.require_login
def exit_trade(trade_id):
    """Close an existing trade and return result as JSON"""

    return operations.exit_trade(trade_id=trade_id)
