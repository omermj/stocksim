from flask import redirect, render_template, flash, Blueprint, url_for, request, jsonify, g
from trades.models import db, Trade
from trades.forms import NewTradeForm

trades = Blueprint("trades", __name__, template_folder="templates")


@trades.route("/")
def user_home():
    return "Trade route"


@trades.route("/new", methods=["GET", "POST"])
def new_trade():
    """Show New Trade form
    
    If form is submitted, validate and enter the trade."""

    # Validate if user is logged in
    if not g.user:
        flash("You do not have permission to view this page.", "danger")
        return redirect(url_for("auth.login"))

    if request.method == "GET":
        form = NewTradeForm()
        return render_template("new_trade.html", form=form)

    if request.method == "POST":

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

