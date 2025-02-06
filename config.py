"""
Configuration module for application settings.

This module defines the `Config` class, which contains configuration 
settings for the database and JWT authentication.
"""
import os

class Config:
    """
    Configuration settings for the application.
    """
    SQLALCHEMY_DATABASE_URI = 'sqlite:///library.db'
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "secret_key")

    def get_config(self):
        """
        Returns the configuration as a dictionary.
        """
        return {
            'SQLALCHEMY_DATABASE_URI': self.SQLALCHEMY_DATABASE_URI,
            'JWT_SECRET_KEY': self.JWT_SECRET_KEY
        }

    def display_config(self):
        """
        Displays the current configuration values.
        """
        print(f"SQLAlchemy Database URI: {self.SQLALCHEMY_DATABASE_URI}")
        print(f"JWT Secret Key: {self.JWT_SECRET_KEY}")
