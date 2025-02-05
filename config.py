"""
Configuration module for application settings.

This module defines the `Config` class, which contains configuration 
settings for the database and JWT authentication.

Attributes:
    SQLALCHEMY_DATABASE_URI (str): Specifies the database location.
    JWT_SECRET_KEY (str): Defines the secret key for JWT authentication.
"""
import os

class Config: # pylint: disable=too-few-public-methods
    """
    Configuration settings for the application.

    Attributes:
        SQLALCHEMY_DATABASE_URI (str): The database URI for SQLAlchemy.
        JWT_SECRET_KEY (str): The secret key for JWT authentication, 
            retrieved from the environment variable `JWT_SECRET_KEY`. 
            Defaults to "secret_key" if not set.
    """
    SQLALCHEMY_DATABASE_URI = 'sqlite:///library.db'
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "secret_key")
