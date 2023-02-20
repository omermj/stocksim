from db import db


class Watchlist(db.Model):
    """Watchlist model"""

    __tablename__ = "watchlists"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        "users.id", ondelete="CASCADE"))

    stocks = db.relationship(
        "Stock", secondary="watchlists_stocks", backref="watchlists")



