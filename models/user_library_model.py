"""
This module defines the `UserLibraryModel` class, which represents the user's 
library in the database.
It tracks the books that users have in their library along with the reading status 
(e.g., "reading", "finished").

Modules:
    - db: SQLAlchemy instance to interact with the database.
    - UserModel: Represents the user who owns the library.
    - BookModel: Represents the book that is part of the user's library.

Classes:
    - UserLibraryModel: Represents a record in the user's library with attributes such as the user,
      the book, and the reading status.
"""
from models import db

class UserLibraryModel(db.Model):
    """
    Represents a user's library, which stores the books associated with a user and their 
    reading status.

    Attributes:
        id (int): The unique identifier of the user-library relationship.
        user_id (int): The ID of the user who owns the library entry.
        book_id (int): The ID of the book that is part of the user's library.
        status (str): The status of the book (e.g., 'reading', 'finished').

    Relationships:
        user (UserModel): The user who owns the library entry, accessed through 'library' backref.
        book (BookModel): The book associated with this user library entry, accessed through 
        'user_libraries' backref.
    
    Methods:
        __init__(user_id, book_id, status): Initializes a new instance of the UserLibraryModel.
        update_status(status): Updates the reading status of a book in the user's library.
        get_user_books(user_id): Returns all books in a user's library.
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

        Args:
            user_id (int): The ID of the user who owns the book in the library.
            book_id (int): The ID of the book in the library.
            status (str): The reading status of the book (e.g., 'reading', 'finished').
        """
        self.user_id = user_id
        self.book_id = book_id
        self.status = status

    def update_status(self, status):
        """
        Updates the reading status of a book in the user's library.

        This method allows the status of a book (e.g., 'reading', 'finished') 
        to be updated for a user.

        Args:
            status (str): The new reading status of the book.
        
        Returns:
            None: Updates the status field in the database.
        """
        self.status = status
        db.session.commit()

    def get_user_books(self, user_id):
        """
        Returns a list of books that belong to the specified user.

        Args:
            user_id (int): The ID of the user whose library books should be retrieved.
        
        Returns:
            list: A list of books in the user's library along with their statuses.
        """
        return UserLibraryModel.query.filter_by(user_id=user_id).all()
