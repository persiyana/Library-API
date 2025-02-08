"""
Tests for the BookModel class and related functionality.
"""
import pytest
from sqlalchemy.exc import SQLAlchemyError
from models.review_model import ReviewModel
from models.book_model import BookModel
from models.user_model import UserModel
from models import db

def test_create_book(book):
    """Test creating and saving a book."""
    assert book.title == "Test Book"
    assert book.author == "Test Author"
    assert book.genre == "Fiction"
    assert book.average_rating == 0.0

def test_update_average_rating(book, review, test_app_client):
    """Test updating the average rating after adding reviews."""
    db.session.add(review)
    db.session.flush()

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

def test_update_average_rating_error(book, monkeypatch):
    """Test handling of database errors when updating average rating."""

    user = UserModel(name="Test User", email="test@gmail.com", password = "test123")
    db.session.add(user)
    db.session.commit()

    review = ReviewModel(book_id=book.id, rating=4.0, user_id=user.id)
    db.session.add(review)
    db.session.commit()

    def mock_commit():
        raise SQLAlchemyError("Database commit error")

    monkeypatch.setattr(db.session, "commit", mock_commit)

    with pytest.raises(RuntimeError,
                       match="Database error while updating rating: Database commit error"):
        book.update_average_rating()


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

def test_create_book_missing_fields():
    """Test handling of missing required fields when creating a book."""

    incomplete_data = {
        "author": "Test Author",
        "genre": "Fiction"
    }

    with pytest.raises(ValueError, match="Missing required field: 'title'"):
        BookModel(incomplete_data)

def test_search_books_database_error(monkeypatch, test_app_client):
    """Test handling of database errors when searching for books."""
    class MockQuery:
        """
        A mock class that simulates the behavior of a SQLAlchemy query for testing purposes.
        """
        def filter(self, *args, **kwargs):
            """
            Simulates the filtering operation of a SQLAlchemy query.
            """
            _ = (args, kwargs)
            raise SQLAlchemyError("Database query error")

        def all(self):
            """
            Simulates the 'all' method of a SQLAlchemy query.
            """
            raise SQLAlchemyError("Database error while fetching all results")

    with test_app_client.application.app_context():
        monkeypatch.setattr(BookModel, "query", MockQuery())
        with pytest.raises(RuntimeError, match="Database error while searching books"):
            BookModel.search_books(title="Test Book")

def test_search_books_no_results(book):
    """Test searching for books that don't exist."""
    _ = book
    search_results = BookModel.search_books(title="Nonexistent Book")
    assert len(search_results) == 0

def test_invalid_review_rating(book, monkeypatch):
    """Test handling of invalid review ratings (ratings outside the range of 1-5)."""
    _ = monkeypatch

    user = UserModel(name="Test User", email="test@gmail.com", password="test123")
    db.session.add(user)
    db.session.commit()

    invalid_review = ReviewModel(book_id=book.id, rating=6.0, user_id=user.id)
    db.session.add(invalid_review)
    db.session.commit()

    book.update_average_rating()
    assert book.average_rating == 6.0


def test_update_average_rating_no_reviews(book):
    """Test handling of no reviews for a book when updating the average rating."""

    with pytest.raises(ValueError, match=f"No reviews found for the book with ID {book.id}."):
        book.update_average_rating()

def test_update_average_rating_unexpected_error(book, monkeypatch):
    """Test handling of unexpected errors (like database rollback) when updating average rating."""

    review = ReviewModel(book_id=book.id, rating=4.0, user_id=1)
    db.session.add(review)
    db.session.commit()

    def mock_commit():
        raise SQLAlchemyError("Database commit error")

    monkeypatch.setattr(db.session, "commit", mock_commit)

    with pytest.raises(RuntimeError,
                       match="Database error while updating rating: Database commit error"):
        book.update_average_rating()

def test_update_average_rating_no_reviews_with_logging(book, caplog):
    """Test handling of no reviews when updating the average rating with logging."""

    with caplog.at_level("ERROR"):
        with pytest.raises(ValueError):
            book.update_average_rating()

    assert "No reviews found for the book" in caplog.text
