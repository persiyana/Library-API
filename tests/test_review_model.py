"""
This module contains test cases for the review functionality in the Flask application.
"""
import pytest
from models import db
from models.review_model import ReviewModel
from models.book_model import BookModel
from models.user_model import UserModel
from main import create_app

@pytest.fixture(name="app")
def app_fixture():
    """Create a Flask app instance for testing."""
    app = create_app("testing")
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(name="test_client")
def test_client_fixture(app):
    """Create a test client."""
    return app.test_client()

@pytest.fixture(name="sample_user")
def sample_user_fixture():
    """Creates a sample user"""
    user = UserModel(name="test_user", email="test@example.com", password="securepassword")
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture(name="sample_book")
def sample_book_fixture():
    """Creates a sample book"""
    book = BookModel({'title': "Test Book", 'author':"Test Author", 'genre': "test"})
    db.session.add(book)
    db.session.commit()
    return book

def test_create_review(test_client, sample_user, sample_book):
    """Test creating a new review"""
    _ = test_client
    review = ReviewModel(user_id=sample_user.id,
                         book_id=sample_book.id,
                         rating=4,
                         review_text="Great book!")
    db.session.add(review)
    db.session.commit()

    fetched_review = ReviewModel.query.filter_by(user_id=sample_user.id,
                                                 book_id=sample_book.id).first()
    assert fetched_review is not None, "Review should exist in the database"
    assert fetched_review.rating == 4
    assert fetched_review.review_text == "Great book!"

def test_save_review(test_client, sample_user, sample_book, mocker):
    """Test saving/updating a review and updating book average rating"""
    _ = test_client
    review = ReviewModel(user_id=sample_user.id,
                         book_id=sample_book.id,
                         rating=3,
                         review_text="Good book")
    db.session.add(review)
    db.session.commit()

    mocker.patch.object(BookModel, "update_average_rating", return_value=None)

    review.save_review(5, "Excellent book")
    updated_review = ReviewModel.query.filter_by(user_id=sample_user.id,
                                                 book_id=sample_book.id).first()

    assert updated_review is not None, "Review should exist after update"
    assert updated_review.rating == 5
    assert updated_review.review_text == "Excellent book"

def test_get_review_details(test_client, sample_user, sample_book):
    """Test retrieving review details"""
    _ = test_client
    review = ReviewModel(user_id=sample_user.id,
                         book_id=sample_book.id,
                         rating=5,
                         review_text="Awesome read")
    db.session.add(review)
    db.session.commit()

    details = review.get_review_details()
    assert details["id"] is not None
    assert details["user_id"] == sample_user.id
    assert details["book_id"] == sample_book.id
    assert details["rating"] == 5
    assert details["review_text"] == "Awesome read"
