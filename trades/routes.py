from flask import redirect, render_template, flash, Blueprint, url_for, request, jsonify, g
from trades.models import db, Trade
from trades.forms import NewTradeForm

trades = Blueprint("trades", __name__, template_folder="templates")


@trades.route("/")
def user_home():
    return "Trade route"


@trades.route("/new")
def show_new_trade_form():
    """Show New Trade form

    If form is submitted, validate and enter the trade."""

    # Validate if user is logged in
    if not g.user:
        flash("You do not have permission to view this page.", "danger")
        return redirect(url_for("auth.login"))

    # Show the form
    form = NewTradeForm()
    return render_template("new_trade.html", form=form)


####################################################################
################# RESTful API Routes ###############################
####################################################################

@trades.route("/", methods=["POST"])
def enter_new_trade():
    """Enter new trade"""

    # Get data from request
    symbol = request.json["symbol"]
    type = request.json["type"]
    qty = request.json["qty"]
    user_id = g.user.id

    # Enter the trade
    response = Trade.enter_trade(symbol=symbol, trade_type=type,
                                 qty=qty, user_id=user_id)

    if response != False:
        return jsonify({"result": "successful",
                        "trade_id": response.id,
                        "symbol": response.symbol,
                        "type": response.trade_type,
                        "qty": response.qty,
                        "entry_price": response.entry_price
                        })

    else:
        return jsonify({"result": "unsuccessful"})


@trades.route("/<int:trade_id>", methods=["PUT"])
def exit_trade(trade_id):
    """Exit trade by changing the trade status to close and updating the latest 
    price and exit date"""

    # Exit trade
    trade = Trade.query.get(trade_id)

    # Update user account balance
    if trade.user.account_balance + trade.get_pnl() <= 0:
        trade.user.account_balance = 0
    else:
        trade.user.account_balance += trade.get_pnl()

    if trade.exit_trade():
        return jsonify({"result": "successful",
                        "trade_id": trade.id,
                        "symbol": trade.symbol,
                        "type": trade.trade_type,
                        "qty": trade.qty,
                        "entry_price": trade.entry_price,
                        "exit_price": trade.latest_price,
                        "exit_date": trade.exit_date,
                        "pnl": trade.get_pnl(),
                        "account_balance": trade.user.account_balance
                        })
    else:
        return jsonify({"result": "unsuccessful"})
