from app import app
import os
from users.models import User
from db import db
from unittest import TestCase

os.environ['DATABASE_URL'] = "postgresql:///stocksim-test"

db.create_all()


class UserModelTestCase(TestCase):
    """Tests for User Model"""

    def setUp(self):
        """Create test client and sample data"""
        app.config['TESTING'] = True
        app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
        app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql:///stocksim-test'

        User.query.delete()

        self.client = app.test_client()

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

    def test_signup(self):
        """Test User Signup"""

        # Number of users before signup
        number_users_before_signup = len(User.query.all())

        user3 = User.signup(
            username="user3",
            email="test3@test.com",
            password="abc123456",
            first_name="Test First Name",
            last_name="Test Last Name"
        )
        number_users_after_signup = len(User.query.all())

        self.assertEqual(number_users_before_signup + 1,
                         number_users_after_signup)

        self.assertIsInstance(user3, User)

    def test_authenticate(self):
        """Test password authentication"""

        user4 = User.signup(
            username="user4",
            email="test3@test.com",
            password="abc123456",
            first_name="Test First Name",
            last_name="Test Last Name"
        )

        result = User.authenticate(username=user4.username,
                                   password=user4.password)

        self.assertIsInstance(user4, User)

    def test_change_password(self):
        """Test change password method"""

        current_password = "abc123456"
        user4 = User.signup(
            username="user4",
            email="test3@test.com",
            password=current_password,
            first_name="Test First Name",
            last_name="Test Last Name"
        )

        new_password = "newpassword123"
        user4.change_password(user4.username, current_password, new_password)

        user = user4.authenticate(user4.username, new_password)

        self.assertIsInstance(user, User)

    def test_edit_profile(self):
        """Test edit profile"""

        self.user_1.edit_profile(email="user1@email.com",
                                 first_name="User1 New",
                                 last_name="User1 New Last")

        self.assertEqual(self.user_1.email, "user1@email.com")
        self.assertEqual(self.user_1.first_name, "User1 New")
        self.assertEqual(self.user_1.last_name, "User1 New Last")

    def test_depost_funds(self):
        """Test deposit funds"""

        balance = self.user_1.account_balance

        self.user_1.deposit_funds(10000)
        self.assertTrue(self.user_1.account_balance, balance + 10000)

    def test_withdraw_funds(self):
        """Test withdraw funds"""

        balance = self.user_1.account_balance

        self.user_1.withdraw_funds(10000)
        self.assertTrue(self.user_1.account_balance, balance - 10000)
