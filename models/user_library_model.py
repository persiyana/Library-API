"""
This module defines the `UserLibraryModel` class, which represents the user's 
library in the database.
It tracks the books that users have in their library along with the reading status 
(e.g., "reading", "finished").
"""
import logging
from typing import TYPE_CHECKING
from sqlalchemy.exc import SQLAlchemyError
from models import db
from utils.validators import validate_required_fields

if TYPE_CHECKING:
    from flask_sqlalchemy.model import Model
else:
    Model = db.Model

class UserLibraryModel(Model):
    """
    Represents a user's library, which stores the books associated with a user and their 
    reading status.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_model.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book_model.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False)

    user = db.relationship('UserModel', backref=db.backref('library', lazy=True))

    valid_statuses = ['reading', 'completed', 'wishlist']

    def __init__(self, user_id, book_id, status):
        """
        Initializes a new UserLibraryModel instance with the provided details.
        """
        validate_required_fields(user_id = user_id, book_id = book_id, status = status)

        self.user_id = user_id
        self.book_id = book_id
        if status not in self.valid_statuses:
            raise ValueError(
                f"Invalid status value: '{status}'. Must be one of {self.valid_statuses}."
                )

        self.status = status

    def update_status(self, status):
        """
        Updates the reading status of a book in the user's library.

        This method allows the status of a book (e.g., 'reading', 'completed') 
        to be updated for a user.
        """
        try:
            if status not in self.valid_statuses:
                raise ValueError(
                    f"Invalid status value: '{status}'. Must be one of {self.valid_statuses}."
                    )

            self.status = status
            db.session.add(self)
            db.session.commit()

        except ValueError as e:
            logging.error("ValueError error: %s", str(e))
            raise

        except SQLAlchemyError as e:
            db.session.rollback()
            logging.error("Database error: %s", str(e))
            raise ValueError(
                "An error occurred while updating the status. Please try again.") from e

        except Exception as e:
            db.session.rollback()
            logging.error("Unexpected error: %s", str(e))
            raise ValueError("An unexpected error occurred. Please try again.") from e

    def get_user_books(self, user_id):
        """
        Returns a list of books that belong to the specified user.
        """
        books = UserLibraryModel.query.filter_by(user_id=user_id).all()
        return books
