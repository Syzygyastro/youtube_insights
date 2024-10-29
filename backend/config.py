# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_default_secret_key')
    SESSION_COOKIE_NAME = 'youtube_analytics_session'
    # Add other configuration variables as needed

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
