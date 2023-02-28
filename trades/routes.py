from flask import redirect, render_template, flash, Blueprint, url_for, request, jsonify, g
from trades.models import db, Trade
from trades.forms import NewTradeForm
from auth.login import Login

trades = Blueprint("trades", __name__, template_folder="templates")


@trades.route("/")
def user_home():
    return "Trade route"


@trades.route("/new")
@Login.require_login
def show_new_trade_form():
    """Show New Trade form

    If form is submitted, validate and enter the trade."""

    # Show the form
    form = NewTradeForm()
    return render_template("new_trade.html", form=form)


####################################################################
################# RESTful API Routes ###############################
####################################################################

@trades.route("/new", methods=["POST"])
@Login.require_login
def enter_new_trade():
    """Enter new trade"""

    # Create the trade
    response = Trade.enter_trade(symbol=request.json["symbol"],
                                 trade_type=request.json["type"],
                                 qty=request.json["qty"],
                                 user_id=g.user.id)

    # If successful, return trade info as JSON. Else return error as JSON
    if isinstance(response, Trade):
        return jsonify(response.to_dict())
    else:
        return jsonify(response)


@trades.route("/<int:trade_id>")
@Login.require_login
def show_trade_details(trade_id):
    """Show trade details"""

    # Update latest stock prices
    Trade.update_latest_prices()

    # Get the trade
    trade = Trade.query.get(trade_id)

    return render_template("trade_details.html", trade=trade)


@trades.route("/<int:trade_id>/close", methods=["PUT"])
@Login.require_login
def exit_trade(trade_id):
    """Close trade by changing the trade status to close and updating the latest 
    price and exit date"""

    # Get trade
    trade = Trade.query.get(trade_id)

    # Close trade
    if trade.close():
        # flash("Trade is successfully closed.", "success")
        # return redirect(url_for("trades.show_trade_details", trade_id=trade.id))
        return jsonify({"result": "success"})
    else:
        return jsonify({"result": "error"})
        # flash("There was an error closing the trade. Please try again.", "danger")
        # return redirect(url_for("trades.show_trade_details", trade_id=trade.id))

    # if trade.exit_trade():
    #     return jsonify({"result": "successful",
    #                     "trade_id": trade.id,
    #                     "symbol": trade.symbol,
    #                     "type": trade.trade_type,
    #                     "qty": trade.qty,
    #                     "entry_price": trade.entry_price,
    #                     "exit_price": trade.latest_price,
    #                     "exit_date": trade.exit_date,
    #                     "pnl": trade.get_pnl(),
    #                     "account_balance": trade.user.account_balance,
    #                     "user_id": trade.user.id
    #                     })
    # else:
    #     return jsonify({"result": "unsuccessful"})


@trades.route("/open")
def show_open_positions():
    """Show all open positions for the logged in user"""

    # Validate if user is logged in
    if not g.user:
        flash("You do not have permission to view this page.", "danger")
        return redirect(url_for("auth.login"))

    return render_template("open_positions.html", trades=g.user.trades)


@trades.route("/history")
def show_trading_history():
    """Show all trading history for the logged in user"""

    # Validate if user is logged in
    if not g.user:
        flash("You do not have permission to view this page.", "danger")
        return redirect(url_for("auth.login"))

    return render_template("history.html", trades=g.user.trades)
