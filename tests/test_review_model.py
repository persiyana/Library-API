"""
This module contains test cases for the review functionality in the Flask application.
"""
import pytest
from sqlalchemy.exc import SQLAlchemyError
from models import db
from models.review_model import ReviewModel
from models.book_model import BookModel

def test_create_review(test_client2, sample_user, sample_book):
    """Test creating a new review"""
    _ = test_client2
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

def test_missing_user_id():
    """Test creating a review without a user_id."""
    with pytest.raises(ValueError, match="Missing required field: 'user_id'"):
        ReviewModel(user_id=None, book_id=1, rating=4, review_text="Good book")

def test_missing_book_id():
    """Test creating a review without a book_id."""
    with pytest.raises(ValueError, match="Missing required field: 'book_id'"):
        ReviewModel(user_id=1, book_id=None, rating=4, review_text="Good book")

def test_missing_rating_and_review_text():
    """Test creating a review without both rating and review_text."""
    with pytest.raises(ValueError, match="You should put either 'rating' or 'review_test' field"):
        ReviewModel(user_id=1, book_id=1, rating=None, review_text=None)

def test_save_review(test_client2, sample_user, sample_book, mocker):
    """Test saving/updating a review and updating book average rating"""
    _ = test_client2
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

def test_save_review_invalid_rating(test_client2, sample_user, sample_book):
    """Test saving a review with an invalid rating."""
    _ = test_client2
    review = ReviewModel(user_id=sample_user.id,
                         book_id=sample_book.id,
                         rating=3,
                         review_text="Good book")
    db.session.add(review)
    db.session.commit()

    with pytest.raises(ValueError, match="Rating must be between 1 and 5."):
        review.save_review(0, "Bad rating")

    with pytest.raises(ValueError, match="Rating must be between 1 and 5."):
        review.save_review(6, "Bad rating")

def test_save_review_missing_book(test_client2, sample_user):
    """Test saving a review when the associated book does not exist."""
    _ = test_client2
    review = ReviewModel(user_id=sample_user.id,
                         book_id=9999,
                         rating=4,
                         review_text="Good book")
    db.session.add(review)
    db.session.commit()

    with pytest.raises(ValueError, match="Book with ID 9999 not found."):
        review.save_review(5, "Great book!")

def test_get_review_details(test_client2, sample_user, sample_book):
    """Test retrieving review details"""
    _ = test_client2
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

def test_save_review_database_error(test_client2, sample_user, sample_book, mocker):
    """Test saving a review and handling database errors."""
    _ = test_client2
    review = ReviewModel(user_id=sample_user.id,
                         book_id=sample_book.id,
                         rating=4,
                         review_text="Good book")
    db.session.add(review)
    db.session.commit()

    mocker.patch.object(db.session, "commit", side_effect=SQLAlchemyError("Database error"))

    with pytest.raises(ValueError,
                       match="An error occurred while saving the review. Please try again."):
        review.save_review(5, "Great book!")

def test_save_review_unexpected_error(test_client2, sample_user, sample_book, mocker):
    """Test saving a review and handling unexpected errors."""
    _ = test_client2
    review = ReviewModel(user_id=sample_user.id,
                         book_id=sample_book.id,
                         rating=4,
                         review_text="Good book")
    db.session.add(review)
    db.session.commit()

    mocker.patch.object(db.session, 'commit', side_effect=Exception("Unexpected error"))

    with pytest.raises(ValueError, match="An unexpected error occurred. Please try again."):
        review.save_review(5, "Great book!")
