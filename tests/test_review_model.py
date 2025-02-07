"""
This module contains test cases for the review functionality in the Flask application.
"""
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
