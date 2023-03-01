from db import db
from alpaca.trading.client import TradingClient

# TODO: Move KEYS TO SEPARATE FILE
API_KEY = "PK0GRC1UBR3JTTNCPQA6"
SECRET_KEY = "qZEepGAYXleOWXlH4B7C3vzYuDgXNrsRVa3ymNxn"


class Stock(db.Model):
    """Stocks model"""

    __tablename__ = "stocks"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    symbol = db.Column(db.String, nullable=False, unique=True)
    name = db.Column(db.String, nullable=False)

    trades = db.relationship("Trade", backref="stock")

    @classmethod
    def create(cls, symbol):
        """Gets company's name from Alpaca API and creates stock

        Returns stock if successful, else returns False."""

        # Check if stock already exists in table. If yes, then return stock
        stock = Stock.query.filter(Stock.symbol==symbol).first()
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


class Watchlist_Stock(db.Model):
    """Connection of a watchlist <-> stock"""

    __tablename__ = "watchlists_stocks"

    watchlist_id = db.Column(db.Integer, db.ForeignKey(
        "watchlists.id", ondelete="cascade"), primary_key=True)

    stock_id = db.Column(db.Integer, db.ForeignKey(
        "stocks.id", ondelete="cascade"), primary_key=True)


