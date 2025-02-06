"""
This module defines the `UserLibraryModel` class, which represents the user's 
library in the database.
It tracks the books that users have in their library along with the reading status 
(e.g., "reading", "finished").
"""
from models import db

class UserLibraryModel(db.Model):
    """
    Represents a user's library, which stores the books associated with a user and their 
    reading status.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_model.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book_model.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False)

    user = db.relationship('UserModel', backref=db.backref('library', lazy=True))
    book = db.relationship('BookModel', backref=db.backref('user_libraries', lazy=True))

    def __init__(self, user_id, book_id, status):
        """
        Initializes a new UserLibraryModel instance with the provided details.
        """
        self.user_id = user_id
        self.book_id = book_id
        self.status = status

    def update_status(self, status):
        """
        Updates the reading status of a book in the user's library.

        This method allows the status of a book (e.g., 'reading', 'finished') 
        to be updated for a user.
        """

        self.status = status
        db.session.add(self)
        db.session.commit()

    def get_user_books(self, user_id):
        """
        Returns a list of books that belong to the specified user.
        """
        return UserLibraryModel.query.filter_by(user_id=user_id).all()
