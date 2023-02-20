class Config(object):
    """Configuration for the app"""
    
    SQLALCHEMY_DATABASE_URI = 'postgresql:///stocksim_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SECRET_KEY = "abcdefghijk"
    DEBUG_TB_INTERCEPT_REDIRECTS = False