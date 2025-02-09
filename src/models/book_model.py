"""
This module defines the `BookModel` class, which represents the structure of a book in the database.
It is used to interact with the `books` table in the database, allowing CRUD operations, 
rating updates, and book search.
"""
import logging
from typing import TYPE_CHECKING
from sqlalchemy.exc import SQLAlchemyError
from src.models import db
from src.models.review_model import ReviewModel
from src.utils.validators import validate_required_fields

if TYPE_CHECKING:
    from flask_sqlalchemy.model import Model
else:
    Model = db.Model

class BookModel(Model):
    """
    Represents a book in the library with its details, reviews, and average rating.
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    average_rating = db.Column(db.Float, default=0.0)
    reviews = db.relationship(
        'ReviewModel',
        back_populates='book',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    user_libraries = db.relationship('UserLibraryModel',
                                     backref='book',
                                     cascade='all, delete-orphan',
                                     lazy=True)

    def __init__(self, book_data):
        """
        Initializes a new BookModel instance with the provided details.
        Ensures required fields ('title', 'author', 'genre') are provided.
        """
        title = book_data.get('title')
        author = book_data.get('author')
        genre = book_data.get('genre')

        validate_required_fields(title = title, author = author, genre = genre)

        self.author = author
        self.title = title
        self.genre = genre
        self.description = book_data.get('description')
        self.average_rating = book_data.get('average_rating', 0.0)



    def update_average_rating(self):
        """
        Updates the average rating of the book based on all reviews.

        This method queries all reviews for the book, extracts their ratings, and recalculates 
        the average rating.
        If there are no ratings, the average rating is set to 0.0.

        Commits the updated rating to the database.
        """
        try:
            reviews = ReviewModel.query.filter_by(book_id=self.id).all()
            if not reviews:
                raise ValueError(f"No reviews found for the book with ID {self.id}.")

            ratings = [review.rating for review in reviews if review.rating is not None]
            self.average_rating = sum(ratings) / len(ratings) if ratings else 0.0
            db.session.commit()
        except ValueError as e:
            logging.error("ValueError: %s", str(e))
            raise
        except SQLAlchemyError as e:
            db.session.rollback()
            logging.error("Database error while updating rating: %s", str(e))
            raise RuntimeError(f"Database error while updating rating: {str(e)}") from e

    @classmethod
    def search_books(cls, title=None, author=None, genre=None):
        """
        Searches for books based on the provided search criteria.
        """
        try:
            query = cls.query
            if title:
                query = query.filter(cls.title.ilike(f"%{title}%"))
            if author:
                query = query.filter(cls.author.ilike(f"%{author}%"))
            if genre:
                query = query.filter(cls.genre.ilike(f"%{genre}%"))
            results = query.all()
            return results
        except SQLAlchemyError as e:
            logging.error("Database error while searching books: %s", str(e))
            raise RuntimeError(f"Database error while searching books: {str(e)}") from e
