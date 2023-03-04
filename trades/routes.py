from flask import redirect, render_template, flash, Blueprint, url_for, request, jsonify, g
from trades.models import Trade
from trades.forms import NewTradeForm
from auth.login import Login
from stocks.models import Stock

trades = Blueprint("trades", __name__,
                   template_folder="templates", static_folder="static")


@trades.route("/")
def user_home():
    return "Trade route"


@trades.route("/new")
@Login.require_login
def show_new_trade_form():
    """Show New Trade form

    If form is submitted, validate and enter the trade."""

    # Get stock id if provided and create data dict, which will be passed to form
    stock_id = request.args.get("stockid")
    if stock_id:
        symbol = Stock.query.get(stock_id).symbol
        data = {"symbol": symbol}
    else:
        data = {}

    # Show the form
    form = NewTradeForm(data=data)
    return render_template("new_trade.html", form=form)


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


@trades.route("/open")
@Login.require_login
def show_open_positions():
    """Show all open positions for the logged in user"""

    open_trades = Trade.query.filter(
        (Trade.user_id == g.user.id) & (Trade.status == "open")).order_by(Trade.entry_date.desc()).all()

    return render_template("open_positions.html", trades=open_trades)


@trades.route("/history")
@Login.require_login
def show_trading_history():
    """Show all trading history for the logged in user"""

    closed_trades = Trade.query.filter(
        (Trade.user_id == g.user.id) & (Trade.status == "closed")).order_by(Trade.entry_date.desc()).all()

    return render_template("history.html", trades=closed_trades)
