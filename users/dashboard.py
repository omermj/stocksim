from users.models import User
from trades.models import Trade


class Dashboard(object):
    """User Dashboard Object"""

    def __init__(self, user_id):
        """Constructor for dashboard"""

        Trade.update_latest_prices()

        self.user = User.query.get(user_id)

        self.open_trades = Trade.query.filter(
            (Trade.user_id == user_id) &
            (Trade.status == "open"))\
            .order_by(Trade.entry_date.desc()).limit(5).all()
        
        self.closed_trades = Trade.query.filter(
            (Trade.user_id == user_id) &
            (Trade.status == "closed"))\
            .order_by(Trade.entry_date.desc()).limit(5).all()
        

