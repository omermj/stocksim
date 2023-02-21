from db import db
from alpaca.data.historical.stock import StockHistoricalDataClient
from alpaca.data.requests import StockSnapshotRequest
from datetime import datetime

# TODO: MOVE API KEYS TO A SEPARATE FILE
API_KEY = "PK0GRC1UBR3JTTNCPQA6"
SECRET_KEY = "qZEepGAYXleOWXlH4B7C3vzYuDgXNrsRVa3ymNxn"


class Trade(db.Model):
    """Trade model"""

    __tablename__ = "trades"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    symbol = db.Column(db.String, nullable=False)
    trade_type = db.Column(db.String, nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    entry_price = db.Column(db.Float, nullable=False)
    exit_price = db.Column(db.Float)
    entry_date = db.Column(db.DateTime, default=datetime.utcnow)
    exit_date = db.Column(db.DateTime)
    status = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        "users.id", ondelete="CASCADE"))

    def __repr__(self):
        """Represent trade"""
        return f"<Trade # {self.id} | Symbol: {self.symbol}> | Type: {self.trade_type} | Qty: {self.qty} | Entry: {self.entry_price}>"

    @classmethod
    def enter_trade(cls, symbol, trade_type, qty, user_id):
        """Enter new trade

        Return new trade if successful, else return False"""

        # Validate quantity
        if not type(qty) is int or qty < 1:
            raise ValueError(
                "qty can only be an integer and must be greater than 0.")

        # Validate trade type
        if not type(trade_type) is str or \
                (trade_type.lower() != "buy" and trade_type.lower() != "sell"):
            raise ValueError(
                "trade_type must be a string and can only be 'buy' or 'sell'.")

        # Get entry price from Alpaca API
        entry_price = cls.get_latest_quote(symbol)

        # TODO: Move exception handling to get_latest_quote function
        if not entry_price:
            raise RuntimeError("Cannot retrieve latest stock price.")

        trade = Trade(symbol=symbol, trade_type=trade_type, qty=qty,
                      entry_price=entry_price, status="open", user_id=user_id)

        try:
            db.session.add(trade)
            db.session.commit()
        except:
            return False
        else:
            return trade

    def exit_trade(self):
        """Exit trade at latest stock price.

        Returns True if successful, else return False"""

        # Get the exit price from Alpaca API
        exit_price = Trade.get_latest_quote(self.symbol)

        if not exit_price:
            raise RuntimeError("Cannot retrieve latest stock price.")

        # Change status to closed
        self.exit_price = exit_price
        self.exit_date = datetime.utcnow
        self.status = "closed"

        try:
            db.session.add(self)
            db.session.commit()
        except:
            return False
        else:
            return True

    @classmethod
    def get_latest_quote(cls, symbol):
        """Calls Alpaca API and get the latest stock quote for symbol

        Returns stock quote if successful, else return False"""

        # Set up the client
        client = StockHistoricalDataClient(
            api_key=API_KEY, secret_key=SECRET_KEY)

        # Structure the request
        symbol = symbol.upper()
        request = StockSnapshotRequest(symbol_or_symbols=symbol)

        # Get the response
        try:
            response = client.get_stock_snapshot(request)
        except:
            return False
        else:
            return response[symbol].latest_trade.price

    @classmethod
    def get_all_trades(status="all"):
        """Returns list of all trades

        Args:
            status (str, optional): "open" returns all open trades
            "closed" returns all closed trades. Defaults to "all".
        """

        if status == "all":
            return Trade.query.all()
        elif status == "open":
            return Trade.query.filter(Trade.status == "open").all()
        elif status == "closed":
            return Trade.query.filter(Trade.status == "closed").all()
        else:
            return None
