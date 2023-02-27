"""Seed file to make sample data for db"""

from db import db
from users.models import User
from trades.models import Trade
from app import app

# Create all tables
db.drop_all()
db.create_all()

# Users
user1 = User.signup(username="omer", email="omer@omer.com",
                    password="omer123", first_name="Omer", last_name="Coder")
user2 = User.signup(username="sidra", email="sidra@omer.com",
                    password="sidra123", first_name="Sidra", last_name="Banker")
user3 = User.signup(username="maryam", email="maryam@omer.com",
                    password="maryam123", first_name="Maryam", last_name="Schooler")
user4 = User.signup(username="mahnoor", email="mahnoor@omer.com",
                    password="mahnoor123", first_name="Mahnoor", last_name="Daycarer")

db.session.add_all([user1, user2, user3, user4])
db.session.commit()

# # Trades
# trade1 = Trade.enter_trade("MSFT", "buy", 100, 1)
# trade2 = Trade.enter_trade("AMZN", "buy", 100, 1)
# trade3 = Trade.enter_trade("AAPL", "sell", 100, 1)
# trade4 = Trade.enter_trade("FSLR", "sell", 100, 1)
# trade5 = Trade.enter_trade("TSLA", "buy", 100, 1)
# trade6 = Trade.enter_trade("MSFT", "buy", 200, 1)
# trade7 = Trade.enter_trade("AAPL", "sell", 50, 1)

# db.session.add_all([trade1, trade2, trade3, trade4, trade5, trade6, trade7])
# db.session.commit()

# # Exit trade
# fslr = Trade.query.filter(Trade.symbol == "FSLR").first()
# fslr.exit_trade()
