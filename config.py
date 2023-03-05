import os

class Config(object):
    """Configuration for the app"""
    
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DATABASE_URL', 'postgresql:///stocksim_db'))
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    SECRET_KEY = "abcdefghijk"
    DEBUG_TB_INTERCEPT_REDIRECTS = False
