"""
This module defines the ReviewModel class, which represents the reviews made by users on books.
The model allows for storing a user's review and rating for a specific book, and updating the book's 
average rating when a new review is saved.

Dependencies:
    - db (SQLAlchemy): Provides the base functionality for the model.
    - UserModel: Represents the user who made the review.
    - BookModel: Represents the book being reviewed.
"""
import importlib
from models import db

class ReviewModel(db.Model):
    """
    Represents a review made by a user for a specific book.

    Attributes:
        id (int): The unique identifier for the review.
        user_id (int): The ID of the user who made the review, linked to the UserModel.
        book_id (int): The ID of the book being reviewed, linked to the BookModel.
        rating (int, optional): The rating given to the book, on a scale from 1 to 5.
        review_text (str, optional): The written review or comments by the user.

    Relationships:
        user (UserModel): The user who created the review, accessed via the 'reviews' backref.
        book (BookModel): The book being reviewed, linked to the book's reviews.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user_model.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book_model.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=True)
    review_text = db.Column(db.Text, nullable=True)

    user = db.relationship('UserModel', backref=db.backref('reviews', lazy=True))
    book = db.relationship('BookModel', back_populates='reviews')

    def __init__(self, user_id, book_id, rating=None, review_text=None):
        """
        Initializes a new instance of the ReviewModel with the provided review details.

        Args:
            user_id (int): The ID of the user who made the review.
            book_id (int): The ID of the book being reviewed.
            rating (int, optional): The rating given by the user. Defaults to None.
            review_text (str, optional): The text of the user's review. Defaults to None.
        """
        self.user_id = user_id
        self.book_id = book_id
        self.rating = rating
        self.review_text = review_text

    def save_review(self, rating, review_text):
        """
        Saves the review with the provided rating and review text. This method updates the
        review in the database and also updates the average rating for the associated book.

        Args:
            rating (int): The rating given to the book, on a scale from 1 to 5.
            review_text (str): The written review or comments for the book.
        
        Side Effects:
            - The review is saved to the database.
            - The average rating of the associated book is updated.
        """
        self.rating = rating
        self.review_text = review_text
        db.session.add(self)
        db.session.commit()

        book_model = importlib.import_module('models.book_model').BookModel

        book = db.session.get(book_model, self.book_id)
        if book:
            book.update_average_rating()

    def get_review_details(self):
        """
        Retrieves the details of the review.

        Returns:
            dict: A dictionary containing the review's id, user_id, book_id, 
            rating, and review_text.
        """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'book_id': self.book_id,
            'rating': self.rating,
            'review_text': self.review_text
        }
