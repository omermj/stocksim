from unittest import TestCase
from db import db
from users.models import User
from watchlists.models import Watchlist
from app import app
import os
os.environ['DATABASE_URL'] = "postgresql:///stocksim-test"


db.create_all()


class WatchlistModelTestCase(TestCase):
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

        self.watchlist_1 = Watchlist(name="Tech",
                                     description="A test watchlist",
                                     user_id=self.user_1.id)

        db.session.add(self.watchlist_1)
        db.session.commit()

    def test_create(self):
        """Test creation of a watchlist"""

        # Good case
        result = Watchlist.create(name="Banks",
                                  description="A test watchlist",
                                  user_id=self.user_1.id)
        self.assertIsInstance(result, Watchlist)

        # Bad case : Name already exists
        result = Watchlist.create(name="Tech",
                                  description="A test watchlist",
                                  user_id=self.user_1.id)
        self.assertNotIsInstance(result, Watchlist)

    def test_remove_watchlist(self):
        """Test removing a watchlist"""

        watchlist = Watchlist.create(name="Banks",
                                     description="Banks watchlist",
                                     user_id=self.user_1.id)

        number_of_watchlists_before = len(self.user_1.watchlists)

        # Test remove
        result = Watchlist.remove(self.watchlist_1)
        self.assertTrue(result)

        # Confirm watchlist is removed
        number_of_watchlists_after = len(self.user_1.watchlists)
        self.assertEqual(number_of_watchlists_before -
                         1, number_of_watchlists_after)

    def test_edit_watchlist(self):
        """Test watchlist edit"""

        self.watchlist_1.edit(new_name="Technology",
                              new_description="My tech watchlist")

        self.assertEqual(self.watchlist_1.name,
                         "Technology")
        self.assertEqual(self.watchlist_1.description,
                         "My tech watchlist")

    def test_add_stock(self):
        """Test Add Stock"""

        # Good case : Correct symbol
        number_of_stocks_before = len(self.watchlist_1.stocks)
        self.watchlist_1.add_stock("MSFT")
        number_of_stocks_after = len(self.watchlist_1.stocks)

        self.assertEqual(number_of_stocks_before + 1, number_of_stocks_after)

        symbols_in_watchlist = [s.symbol for s in self.watchlist_1.stocks]
        self.assertTrue("MSFT" in symbols_in_watchlist)

        # Bad case : Incorrect symbol
        number_of_stocks_before = len(self.watchlist_1.stocks)
        self.watchlist_1.add_stock("erwerw55")
        number_of_stocks_after = len(self.watchlist_1.stocks)

        self.assertEqual(number_of_stocks_before, number_of_stocks_after)

    def test_remove_stock(self):
        """Test removing stock"""

        self.watchlist_1.add_stock("MSFT")
        self.watchlist_1.add_stock("AAPL")

        # Good case : Remove stock which exists in watchlist
        number_of_stocks_before = len(self.watchlist_1.stocks)
        self.watchlist_1.remove_stock("MSFT")
        number_of_stocks_after = len(self.watchlist_1.stocks)

        self.assertEqual(number_of_stocks_before, number_of_stocks_after + 1)

        # Bad case : Remove stock which doest not exist in watchlist
        number_of_stocks_before = len(self.watchlist_1.stocks)
        result = self.watchlist_1.remove_stock("GOOGL")
        number_of_stocks_after = len(self.watchlist_1.stocks)

        self.assertFalse(result)
        self.assertEqual(number_of_stocks_before, number_of_stocks_after)
