from app import app
import os
from watchlists.models import Watchlist
from users.models import User
from db import db
from unittest import TestCase

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

        # # Bad case : Name already exists
        # result = Watchlist.create(name="Tech",
        #                                     description="A test watchlist",
        #                                     user_id=self.user_1.id)
        # self.assertIsInstance(result, Watchlist)
