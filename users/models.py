# from flask_sqlalchemy import SQLAlchemy
from db import db

# db = SQLAlchemy()

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