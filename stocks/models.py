from db import db
from alpaca.trading.client import TradingClient
from alpaca.data.historical.stock import StockHistoricalDataClient
from alpaca.data.requests import StockSnapshotRequest
from alpaca.common import exceptions
from keys import API_KEY, SECRET_KEY
# import os

# API_KEY = os.environ.get("API_KEY")
# SECRET_KEY = os.environ.get("API_SECRET_KEY")


class Stock(db.Model):
    """Stocks model"""

    __tablename__ = "stocks"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    symbol = db.Column(db.String(10), nullable=False, unique=True)
    name = db.Column(db.String, nullable=False)

    trades = db.relationship("Trade", backref="stock")

    @classmethod
    def create(cls, symbol):
        """Gets company's name from Alpaca API and creates stock

        Returns stock if successful, else returns False."""

        # Check if stock already exists in table. If yes, then return stock
        stock = Stock.query.filter(Stock.symbol == symbol).first()
        if stock:
            return stock

        # Get stock name
        name = Stock.get_name(symbol)

        # Add stock if name is valid
        if name:
            try:
                stock = Stock(symbol=symbol, name=name)
                db.session.add(stock)
                db.session.commit()
            except:
                return False
            else:
                return stock
        else:
            return False

    @classmethod
    def get_name(cls, symbol):
        """Get stock name from Alpaca API

        Returns stock name if successful, else return False."""

        trading_client = TradingClient(API_KEY, SECRET_KEY)

        try:
            stock_name = trading_client.get_asset(symbol.upper()).name
        except:
            return False
        else:
            return stock_name

    def get_price(self):
        """Returns latest stock price"""

        # Set up the client
        client = StockHistoricalDataClient(
            api_key=API_KEY, secret_key=SECRET_KEY)

        # Structure the request
        request = StockSnapshotRequest(symbol_or_symbols=self.symbol)

        # Get the response
        try:
            response = client.get_stock_snapshot(request)
        except exceptions.APIError as e:
            return ({"error": {
                    "type": "symbol",
                    "message": "The symbol is not valid."
                    }})
        except Exception as e:
            return ({"error": {
                    "type": "others",
                    "message": "An unknown error has occured. Please try again."
                    }})
        else:
            if response != None:
                return round(response[self.symbol].latest_trade.price, 2)
            else:
                return ({"error": {
                    "type": "symbol",
                    "message": "The symbol is not valid."
                }})


class Watchlist_Stock(db.Model):
    """Connection of a watchlist <-> stock"""

    __tablename__ = "watchlists_stocks"

    watchlist_id = db.Column(db.Integer, db.ForeignKey(
        "watchlists.id", ondelete="cascade"), primary_key=True)

    stock_id = db.Column(db.Integer, db.ForeignKey(
        "stocks.id", ondelete="cascade"), primary_key=True)
