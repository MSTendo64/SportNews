import os
from datetime import datetime

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-123'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///sport_news.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    NEWS_PER_PAGE = 6