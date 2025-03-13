import os

class Config:
    # Secret key for session management and CSRF protection
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # PostgreSQL database configuration
    #format = 'postgresql://username:password@host:port/database_name'
    SQLALCHEMY_DATABASE_URL = os.environ.get('database_url') or 'postgresql://username:password@host:port/database_name'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True

