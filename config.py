# config.py
from datetime import timedelta


class Config:
    SECRET_KEY = "super-secret-key"  # қалаған сөз
    SQLALCHEMY_DATABASE_URI = "sqlite:///app.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = "jwt-secret-key"  # қалаған сөз
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
