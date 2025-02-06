"""
This module defines the `BookModel` class, which represents the structure of a book in the database.
It is used to interact with the `books` table in the database, allowing CRUD operations, 
rating updates, and book search.
"""
from models import db
from models.review_model import ReviewModel

class BookModel(db.Model):
    """
    Represents a book in the library with its details, reviews, and average rating.
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    average_rating = db.Column(db.Float, default=0.0)
    reviews = db.relationship('ReviewModel', back_populates='book', lazy='dynamic')

    def __init__(self, book_data):
        """
        Initializes a new BookModel instance with the provided details.
        """
        self.title = book_data.get('title')
        self.author = book_data.get('author')
        self.genre = book_data.get('genre')
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
        reviews = ReviewModel.query.filter_by(book_id=self.id).all()
        ratings = [review.rating for review in reviews if review.rating is not None]
        self.average_rating = sum(ratings) / len(ratings) if ratings else 0.0
        db.session.commit()

    @classmethod
    def search_books(cls, title=None, author=None, genre=None):
        """
        Searches for books based on the provided search criteria.
        """
        query = cls.query
        if title:
            query = query.filter(cls.title.ilike(f"%{title}%"))
        if author:
            query = query.filter(cls.author.ilike(f"%{author}%"))
        if genre:
            query = query.filter(cls.genre.ilike(f"%{genre}%"))
        return query.all()
