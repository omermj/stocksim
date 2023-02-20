from db import db


class Stock(db.Model):
    """Stocks model"""

    __tablename__ = "stocks"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    symbol = db.Column(db.String, nullable=False, unique=True)
    name = db.Column(db.String, nullable=False)


class Watchlist_Stock(db.Model):
    """Connection of a watchlist <-> stock"""

    __tablename__ = "watchlists_stocks"

    watchlist_id = db.Column(db.Integer, db.ForeignKey(
        "watchlists.id", ondelete="cascade"), primary_key=True)

    stock_id = db.Column(db.Integer, db.ForeignKey(
        "stocks.id", ondelete="cascade"), primary_key=True)


# class Trade_Stock(db.Model):
#     """Connection of a trade <-> stock"""

#     __tablename__ = "trades_stocks"

#     trade_id = db.Column(db.Integer, db.ForeignKey(
#         "trades.id", ondelete="cascade"), primary_key=True)

#     stock_id = db.Column(db.Integer, db.ForeignKey(
#         "stocks.id", ondelete="cascade"), primary_key=True)
