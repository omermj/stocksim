from db import db
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError
from auth.forms import ChangePasswordForm
from flask import render_template, flash, redirect, url_for

bcrypt = Bcrypt()

# Default starting account balance
STARTING_BALANCE = 50000


class User(db.Model):
    """User model"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    account_balance = db.Column(db.Float, nullable=False)

    trades = db.relationship("Trade", backref="user")
    watchlists = db.relationship("Watchlist", backref="user")

    def __repr__(self):
        """Represent user"""
        return f"<User # {self.id}: {self.username}>"

    @classmethod
    def signup(cls, username, email, password, first_name, last_name):
        """Signup new user

        Returns newly added user if successful, else return {"error": "message"}"""

        # Check if username already exists in the database. If yes,
        # return error

        hashed_pwd = bcrypt.generate_password_hash(password).decode("UTF-8")

        try:
            user = User(username=username,
                        password=hashed_pwd,
                        email=email,
                        first_name=first_name,
                        last_name=last_name,
                        account_balance=STARTING_BALANCE)
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            return {"error": "Username already taken"}
        except:
            return {"error": "An error occured while creating the account."}
        else:
            return user

    @classmethod
    def authenticate(cls, username, password):
        """Finds the user in the system and authenticates with the provided
        password.

        Returns user if authenticated, else return False"""

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

    def change_password(self, username, current_password, new_password):
        """Change user password
        Returns True if successful, else returns False"""

        # Authenticate user
        if User.authenticate(username=username,
                             password=current_password) == False:
            return False

        hashed_pwd = bcrypt.generate_password_hash(
            new_password).decode("UTF-8")

        self.password = hashed_pwd

        try:
            db.session.add(self)
            db.session.commit()
        except:
            return False
        else:
            return True

    def edit_profile(self, email, first_name, last_name):
        """Edits user profile
        Returns True if successful, else returns False"""

        self.email = email
        self.first_name = first_name
        self.last_name = last_name

        try:
            db.session.add(self)
            db.session.commit()
        except:
            return False
        else:
            return True

    def deposit_funds(self, amount):
        """Deposit amount to user's account balance

        Returns new account balance if True, else return False"""

        self.account_balance += amount

        try:
            db.session.add(self)
            db.session.commit()
        except:
            return False
        else:
            return self.account_balance

    def withdraw_funds(self, amount):
        """Withdraw amount from user's account balance

        Returns new account balance if True, else return False"""

        if (self.account_balance - amount) > 0:
            self.account_balance -= amount
        else:
            return False

        try:
            db.session.add(self)
            db.session.commit()
        except:
            return False
        else:
            return self.account_balance

    def get_equity(self):
        """Get user equity

        equity = account balance + sum of unrealized PnL for all trades"""

        # Get open trades
        open_trades = [
            trade for trade in self.trades if trade.status == "open"]

        # Calculate value of open trades
        total_pnl = 0
        for trade in open_trades:
            total_pnl += trade.get_pnl()

        # Return equity
        return self.account_balance + total_pnl

    def get_buying_power(self):
        """Get user's available buying power

        Available buying power = account balance - buying power used by all trades"""

        # Get open trades
        open_trades = [
            trade for trade in self.trades if trade.status == "open"]

        # Get total buying power used
        buying_power_used = 0
        for trade in open_trades:
            buying_power_used += trade.get_trade_buying_power()

        # Return buying power available
        return self.account_balance - buying_power_used

    def get_realized_gain(self):
        """Get total realized gain or loss for the user"""

        total = 0
        for trade in self.trades:
            total += trade.get_pnl() if trade.status == "closed" else 0

        return total

    def get_unrealized_gain(self):
        """Get total unrealized gain or loss for the user"""

        total = 0
        for trade in self.trades:
            total += trade.get_pnl() if trade.status == "open" else 0

        return total

    def get_account_growth_percent(self):
        """Get account growth percentage"""

        return (self.account_balance / STARTING_BALANCE - 1)

    def get_equity_growth_percent(self):
        """Get account growth percentage"""

        return (self.get_equity() / STARTING_BALANCE - 1)
