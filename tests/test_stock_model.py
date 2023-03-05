from unittest import TestCase
from db import db
from stocks.models import Stock
from app import app
import os
os.environ['DATABASE_URL'] = "postgresql:///stocksim-test"


db.create_all()


class StockModelTestCase(TestCase):
    """Tests for User Model"""

    def setUp(self):
        """Create test client and sample data"""

        Stock.query.delete()

        self.client = app.test_client()

    def test_create_stock(self):
        """Test create stock"""

        # Good case : Correct symbol
        number_of_stocks_before = len(Stock.query.all())
        result = Stock.create("MSFT")
        number_of_stocks_after = len(Stock.query.all())

        self.assertIsInstance(result, Stock)
        self.assertEqual(number_of_stocks_before + 1, number_of_stocks_after)

    def test_get_name(self):
        """Test retrieval of stock name"""

        name = Stock.get_name("MSFT")
        self.assertIn("Microsoft", name)

