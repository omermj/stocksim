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

    @classmethod
    def create(cls, name, user_id):
        """Create a new watchlist.

        Returns watchlist if successful, else return False"""

        watchlist = Watchlist(name=name, user_id=user_id)

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
            raise RuntimeError(
                "Cannot rename watchlist due to a runtime error.")

    def add_stock(self, stock):
        """Adds stock to the Watchlist.

        Returns True if successful, else return False."""

        self.stocks.append(stock)

        try:
            db.session.add(self)
            db.session.commit()
        except:
            return False
        else:
            return True

    def remove_stock(self, stock):
        """Removes stock from the watchlist.

        Returns True if successful, else return False."""

        try:
            self.stocks.remove(stock)
            db.session.add(self)
            db.session.commit()
        except:
            return False
        else:
            return True
