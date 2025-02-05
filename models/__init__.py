"""
This module sets up and initializes the SQLAlchemy instance for 
database interaction in the Flask application.

The `SQLAlchemy` object is used to interact with the database, 
defining models and performing queries.

Attributes:
    db (SQLAlchemy): The SQLAlchemy instance used for database operations.
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
