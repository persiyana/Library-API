"""
This module contains tests for the BookModel class and related functionality 
such as creating and updating books, adding reviews, and searching books.
"""
import pytest
from models import db
from models.book_model import BookModel
from models.user_model import UserModel
from models.review_model import ReviewModel
from main import create_app


@pytest.fixture(name="test_app_client")
def test_app_client_fixture():
    """Create a test client with a fresh database."""

    app = create_app("testing")

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()


@pytest.fixture(name="book")
def book_fixture(test_app_client):
    """Create a sample book."""
    book_data = {'title': "Test Book", 'author': "Test Author", 'genre': "Fiction"}
    book = BookModel(book_data)
    with test_app_client.application.app_context():
        db.session.add(book)
        db.session.commit()
        db.session.refresh(book)
    return book


@pytest.fixture(name="user")
def user_fixture(test_app_client):
    """Create a sample user."""
    user = UserModel(name="Test User", email="testuser@example.com", password="password123")
    with test_app_client.application.app_context():
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)
    return user


@pytest.fixture(name="review")
def review_fixture(test_app_client, user, book):
    """Create a sample review for a book."""
    review = ReviewModel(user_id=user.id, book_id=book.id,
                         rating=4, review_text="Great book!")
    with test_app_client.application.app_context():
        db.session.add(review)
        db.session.commit()
        db.session.refresh(review)
    return review


def test_create_book(book):
    """Test creating and saving a book."""
    assert book.title == "Test Book"
    assert book.author == "Test Author"
    assert book.genre == "Fiction"
    assert book.average_rating == 0.0


def test_update_average_rating(book, review, test_app_client):
    """Test updating the average rating after adding reviews."""

    book.update_average_rating()

    assert book.average_rating == 4.0

    review2 = ReviewModel(user_id=review.user_id, book_id=book.id,
                          rating=5, review_text="Excellent!")

    with test_app_client.application.app_context():
        db.session.add(review2)
        db.session.commit()
        db.session.refresh(review2)

    book.update_average_rating()

    assert book.average_rating == 4.5


def test_search_books_by_title(book):
    """Test searching books by title."""
    _ = book
    search_results = BookModel.search_books(title="Test Book")
    assert len(search_results) == 1
    assert search_results[0].title == "Test Book"


def test_search_books_by_author(book):
    """Test searching books by author."""
    _ = book
    search_results = BookModel.search_books(author="Test Author")
    assert len(search_results) == 1
    assert search_results[0].author == "Test Author"


def test_search_books_by_genre(book):
    """Test searching books by genre."""
    _ = book
    search_results = BookModel.search_books(genre="Fiction")
    assert len(search_results) == 1
    assert search_results[0].genre == "Fiction"


def test_search_books_multiple_criteria(book):
    """Test searching books by multiple criteria."""
    _ = book
    search_results = BookModel.search_books(title="Test Book",
                                            author="Test Author",
                                            genre="Fiction")
    assert len(search_results) == 1
    assert search_results[0].title == "Test Book"
    assert search_results[0].author == "Test Author"
    assert search_results[0].genre == "Fiction"
