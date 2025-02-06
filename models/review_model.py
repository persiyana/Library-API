"""
This module defines the ReviewModel class, which represents the reviews made by users on books.
The model allows for storing a user's review and rating for a specific book, and updating the book's 
average rating when a new review is saved.
"""
import importlib
from models import db

class ReviewModel(db.Model):
    """
    Represents a review made by a user for a specific book.
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
        """
        self.user_id = user_id
        self.book_id = book_id
        self.rating = rating
        self.review_text = review_text

    def save_review(self, rating, review_text):
        """
        Saves the review with the provided rating and review text. This method updates the
        review in the database and also updates the average rating for the associated book.
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
        """
        return {
            'id': self.id,
            'user_id': self.user_id,
            'book_id': self.book_id,
            'rating': self.rating,
            'review_text': self.review_text
        }
