import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///library.db'
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "secret_key")
