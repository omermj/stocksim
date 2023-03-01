from db import db
from stocks.models import Stock
from trades.models import Trade


class Watchlist(db.Model):
    """Watchlist model"""

    __tablename__ = "watchlists"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    description = db.Column(db.String(50), default="No description")
    user_id = db.Column(db.Integer, db.ForeignKey(
        "users.id", ondelete="CASCADE"))

    stocks = db.relationship(
        "Stock", secondary="watchlists_stocks", backref="watchlists")

    @classmethod
    def create(cls, name, description, user_id):
        """Create a new watchlist.

        Returns watchlist if successful, else return False"""
        if description == "":
            description = "No description"

        watchlist = Watchlist(
            name=name, description=description, user_id=user_id)

        try:
            db.session.add(watchlist)
            db.session.commit()
        except:
            return False
        else:
            return watchlist

    @classmethod
    def remove(cls, watchlist):
        """Remove watchlist.

        Returns True if successful, else return False"""

        try:
            db.session.delete(watchlist)
            db.session.commit()
        except:
            return False
        else:
            return True

    def rename(self, new_name):
        """Rename watchlist"""

        self.name = new_name

        try:
            db.session.add(self)
            db.session.commit()
        except:
            return False

    def add_stock(self, symbol):
        """Adds stock to the Watchlist.

        Returns True if successful, else return False."""

        # Get stock from symbol
        stock = Stock.create(symbol)

        # If stock is valid and stock does not already exists in watchlist,
        # append stock
        if stock != False and stock not in self.stocks:

            self.stocks.append(stock)
            try:
                db.session.add(self)
                db.session.commit()
            except:
                return False
            else:
                return True

        return False

    def remove_stock(self, symbol):
        """Removes stock from the watchlist.

        Returns True if successful, else return False."""

        # Get stock from symbol
        stock = Stock.create(symbol)

        # If stock is valid and stock is in watchlist remove stock
        if stock != False and stock in self.stocks:

            try:
                self.stocks.remove(stock)
                db.session.add(self)
                db.session.commit()
            except:
                return False
            else:
                return True

        return False

    def get_all_stocks(self):
        """Returns a list of all watchlist stocks with latest prices

        [{"symbol": symbol, "name": name, "price": price}]
        """

        # Get list of all symbols
        symbols = [s.symbol for s in self.stocks]

        output = []

        quotes = Trade.get_multiple_quotes(symbols)
        try:
            for symbol in quotes:
                name = Stock.query.filter(Stock.symbol == "MSFT").first().name
                output.append({"symbol": symbol, "name": name,
                               "price": quotes[symbol]})
        except:
            return False
        else:
            return output
