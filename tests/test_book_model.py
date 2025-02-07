"""
Tests for the BookModel class and related functionality.
"""
from models.review_model import ReviewModel
from models.book_model import BookModel
from models import db

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
