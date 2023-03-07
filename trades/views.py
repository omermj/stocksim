from flask import render_template, request, g
from trades.models import Trade
from trades.forms import NewTradeForm
from stocks.models import Stock


class Views(object):
    """Utilities class for Trades"""

    @classmethod
    def show_trade_details(cls, trade_id):
        """Show trade details"""

        # Update latest stock prices
        Trade.update_latest_prices()

        # Get the trade
        trade = Trade.query.get(trade_id)

        return render_template("trade_details.html", trade=trade)

    @classmethod
    def show_open_positions(cls):
        """Show all open positions for the logged in user"""

        open_trades = Trade.query.filter(
            (Trade.user_id == g.user.id) & (Trade.status == "open")).order_by(Trade.entry_date.desc()).all()

        return render_template("open_positions.html", trades=open_trades)

    @classmethod
    def show_trading_history(cls):
        """Show all trading history for the logged in user"""

        closed_trades = Trade.query.filter(
            (Trade.user_id == g.user.id) & (Trade.status == "closed")).order_by(Trade.entry_date.desc()).all()

        return render_template("history.html", trades=closed_trades)

    @classmethod
    def show_new_trade_form(cls):
        """Show new trade form"""

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
