from app import app
import os
from trades.models import Trade
from users.models import User
from db import db
from unittest import TestCase

os.environ['DATABASE_URL'] = "postgresql:///stocksim-test"

db.create_all()


class TradeModelTestCase(TestCase):
    """Tests for User Model"""

    def setUp(self):
        """Create test client and sample data"""

        User.query.delete()

        self.client = app.test_client()

        # Create test users
        self.user_1 = User(
            username="user1",
            password="test123",
            email="test1@test.com",
            first_name="Test First",
            last_name="Test Second",
            account_balance=50000
        )
        self.user_2 = User(
            username="user2",
            password="test456",
            email="test2@test.com",
            first_name="Tset First",
            last_name="Tset Second",
            account_balance=50000
        )

        db.session.add_all([self.user_1, self.user_2])
        db.session.commit()

        # Create test trades
        self.trade_1 = Trade.enter_trade(
            symbol="AMZN",
            trade_type="buy",
            qty=100,
            user_id=self.user_1.id
        )

        db.session.add(self.trade_1)
        db.session.commit()

    def test_enter_trade(self):
        """Test enter trade"""

        # Good case
        trade = Trade.enter_trade(
            symbol="MSFT",
            trade_type="buy",
            qty=100,
            user_id=self.user_1.id
        )
        self.assertIsInstance(trade, Trade)

        # Bad case: Wrong symbol
        trade = Trade.enter_trade(
            symbol="MSFTTTT",
            trade_type="buy",
            qty=100,
            user_id=self.user_1.id
        )
        self.assertNotIsInstance(trade, Trade)

        # Bad case: Wrong qty - High number
        trade = Trade.enter_trade(
            symbol="MSFT",
            trade_type="buy",
            qty=1000000000000000,
            user_id=self.user_1.id
        )
        self.assertNotIsInstance(trade, Trade)

        # Bad case: Wrong qty - Negative number
        trade = Trade.enter_trade(
            symbol="MSFT",
            trade_type="buy",
            qty=-20,
            user_id=self.user_1.id
        )
        self.assertNotIsInstance(trade, Trade)

        # Bad case: Wrong type
        trade = Trade.enter_trade(
            symbol="MSFT",
            trade_type="long",
            qty=20,
            user_id=self.user_1.id
        )
        self.assertNotIsInstance(trade, Trade)

    def test_close(self):
        """Test close trade"""

        result = self.trade_1.close()

        self.assertTrue(result)

    def test_get_latest_quote(self):
        """Test Get Latest Quote - Method which retrieves symbols from API"""

        # Good case : Correct symbol
        result = Trade.get_latest_quote("AAPL")
        self.assertIsInstance(result, float)

        # Bad case : Incorrect symbol
        result = Trade.get_latest_quote("AAPLLLLLL")
        self.assertIsInstance(result, dict)

    def test_get_multiple_quotes(self):
        """Test retrieval of multiple quotes from API"""

        # Good case
        result = Trade.get_multiple_quotes(["AAPL", "MSFT", "NVDA"])
        self.assertIsInstance(result, dict)

        # Bad case : one symbol is incorrect
        result = Trade.get_multiple_quotes(["AAPL", "MMMMMSFT", "NVDA"])
        self.assertFalse(result)