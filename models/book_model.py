"""
This module defines the `BookModel` class, which represents the structure of a book in the database.
It is used to interact with the `books` table in the database, allowing CRUD operations, 
rating updates, and book search.

Modules:
    - db: The SQLAlchemy instance to interact with the database.
    - ReviewModel: The model for reviews related to books.

Classes:
    - BookModel: Represents a book in the library with attributes like title, author, genre, 
    description, and average_rating.
"""
from models import db
from models.review_model import ReviewModel

class BookModel(db.Model):
    """
    Represents a book in the library with its details, reviews, and average rating.

    Attributes:
        id (int): The unique identifier of the book.
        title (str): The title of the book.
        author (str): The author of the book.
        genre (str): The genre of the book.
        description (str): A short description of the book.
        average_rating (float): The average rating of the book, calculated from reviews.
        reviews (relationship): The relationship between the book and its reviews.

    Methods:
        __init__(title, author, genre, description=None, average_rating=0.0): Initializes a new 
        BookModel instance.
        update_average_rating(): Updates the average rating of the book based on its reviews.
        search_books(title=None, author=None, genre=None): Searches for books by title, author, 
        or genre.
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

        Args:
            book_data (dict): A dictionary containing the book details. Keys should include:
                - title (str): The title of the book.
                - author (str): The author of the book.
                - genre (str): The genre of the book.
                - description (str, optional): A short description of the book. Defaults to None.
                - average_rating (float, optional): The average rating of the book. Defaults to 0.0.
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

        Args:
            title (str, optional): The title of the book to search for. Defaults to None.
            author (str, optional): The author of the book to search for. Defaults to None.
            genre (str, optional): The genre of the book to search for. Defaults to None.

        Returns:
            list: A list of books that match the search criteria.
        """
        query = cls.query
        if title:
            query = query.filter(cls.title.ilike(f"%{title}%"))
        if author:
            query = query.filter(cls.author.ilike(f"%{author}%"))
        if genre:
            query = query.filter(cls.genre.ilike(f"%{genre}%"))
        return query.all()
