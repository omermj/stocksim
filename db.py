from flask_sqlalchemy import SQLAlchemy

# Connect to database
db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)