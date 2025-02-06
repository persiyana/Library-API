"""
This module contains tests for the review functionality in the application, 
focusing on adding reviews to books. It ensures that reviews can be added, 
validated, and managed correctly.
"""
import pytest
from flask_jwt_extended import create_access_token
from models import db
from models.book_model import BookModel
from models.review_model import ReviewModel
from models.user_model import UserModel
from main import create_app

@pytest.fixture(name="app")
def app_fixture():
    """Fixture for creating an app instance in testing mode."""
    app = create_app(config="testing")
    yield app

@pytest.fixture(name="client")
def client_fixture(app):
    """Fixture for getting the test client."""
    return app.test_client()

@pytest.fixture(name="db_session")
def db_session_fixture(app):
    """Fixture for setting up a temporary database for testing."""
    with app.app_context():
        db.create_all()
        yield db.session
        db.session.remove()
        db.drop_all()

@pytest.fixture(name="create_user")
def create_user_fixture(db_session):
    """Fixture for creating a user in the database."""
    user = UserModel(name='Test User', email='test@example.com', password='password')
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture(name="create_book")
def create_book_fixture(db_session):
    """Fixture for creating a book in the database."""
    book_data = {
        'title': 'Test Book',
        'author': 'Test Author',
        'genre': 'Fiction',
        'description': 'A test book description',
    }
    book = BookModel(book_data)
    db_session.add(book)
    db_session.commit()
    return book

@pytest.fixture(name="create_review")
def create_review_fixture(db_session, create_user, create_book):
    """Fixture for creating a review in the database."""
    review = ReviewModel(user_id=create_user.id,
                         book_id=create_book.id,
                         rating=4,
                         review_text='Good book!')
    db_session.add(review)
    db_session.commit()
    return review

def test_add_review_success(client, create_user, create_book):
    """Test adding a valid review."""
    access_token = create_access_token(identity=create_user.id)
    response = client.post(
        f'/api/books/{create_book.id}/review/',
        json={'rating': 5, 'review_text': 'Excellent book!'},
        headers={'Authorization': f'Bearer {access_token}'}
    )
    assert response.status_code == 201
    assert response.json == {'message': 'Review added successfully'}

def test_add_review_invalid_rating(client, create_user, create_book):
    """Test adding a review with an invalid rating (less than 1)."""
    access_token = create_access_token(identity=create_user.id)
    response = client.post(
        f'/api/books/{create_book.id}/review/',
        json={'rating': 0, 'review_text': 'Not good!'},
        headers={'Authorization': f'Bearer {access_token}'}
    )
    assert response.status_code == 400
    assert response.json == {'message': 'Rating must be between 1 and 5'}

def test_add_review_already_reviewed(client, create_user, create_book, create_review):
    """Test when the user has already reviewed the book."""
    _ = create_review
    access_token = create_access_token(identity=create_user.id)
    response = client.post(
        f'/api/books/{create_book.id}/review/',
        json={'rating': 3, 'review_text': 'Changed my mind!'},
        headers={'Authorization': f'Bearer {access_token}'}
    )
    assert response.status_code == 400
    assert response.json == {'message': 'You have already reviewed this book'}

def test_add_review_book_not_found(client, create_user):
    """Test adding a review when the book is not found."""
    access_token = create_access_token(identity=create_user.id)
    response = client.post(
        '/api/books/999999/review/',
        json={'rating': 4, 'review_text': 'Not bad.'},
        headers={'Authorization': f'Bearer {access_token}'}
    )
    assert response.status_code == 404
    assert response.json == {'message': 'Book not found'}
