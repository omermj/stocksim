"""Seed file to make sample data for db"""

from db import db
from users.models import User
from trades.models import Trade
from app import app

with app.app_context():
    # Create all tables
    db.drop_all()
    db.create_all()

    # Users
    user1 = User.signup(
        username="testuser",
        email="testuser@mail.com",
        password="test123",
        first_name="Test First",
        last_name="Test Last",
    )

    db.session.add(user1)
    db.session.commit()
