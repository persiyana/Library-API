"""
Configuration and shared fixtures for tests.
"""
import pytest
from flask_jwt_extended import create_access_token
from src.models import db
from src.models.book_model import BookModel
from src.models.user_model import UserModel
from src.models.review_model import ReviewModel
from src.models.user_library_model import UserLibraryModel
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

@pytest.fixture(name="app")
def app_fixture():
    """
    Fixture that initializes the Flask application in testing mode.
    It configures the app to use a test database and provides an app instance for the test cases.
    """
    app = create_app(config="testing")

    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.drop_all()

@pytest.fixture(name="init_db")
def init_db_fixture(app):
    """
    Fixture that initializes the test database with a sample user and book.
    Creates an instance of a user and a book in the database, and yields the database session.
    This ensures a fresh database setup before each test case.
    """
    with app.app_context():
        db.create_all()

        user = UserModel(name="Test User", email="testuser@example.com", password="password123")
        db.session.add(user)
        db.session.commit()

        sample_book = BookModel({
            'title': 'Test Book',
            'author': 'Test Author',
            'genre': 'Test Genre',
            'description': 'Test Description'
        })
        db.session.add(sample_book)
        db.session.commit()

        yield db

        db.session.remove()
        db.drop_all()

@pytest.fixture(name="client")
def client_fixture(app):
    """
    Fixture that provides a test client for sending HTTP requests to the application.

    This fixture initializes the Flask test client which allows simulating HTTP requests 
    to the app during testing. The client can be used to send requests like GET, POST, 
    PATCH, DELETE, etc., and retrieve responses for assertions.
    """
    return app.test_client()

@pytest.fixture(name="access_token")
def access_token_fixture():
    """
    Fixture that creates a JWT token for authenticating requests.
    """
    user = UserModel.query.first()
    assert user is not None, "No user found in the database"
    return create_access_token(identity=user.id)

@pytest.fixture(name="new_user_data")
def new_user_data_fixture():
    """
    Fixture to provide data for creating a new user.

    This fixture returns a dictionary containing the necessary data for registering a new user
    (name, email, and password) that can be used in test cases.
    """
    return {
        'name': 'Test User',
        'email': 'testuser@example.com',
        'password': 'securepassword'
    }


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


@pytest.fixture(scope="module", name="test_client")
def test_client_fixture():
    """
    Fixture that creates a Flask app instance and sets up an in-memory SQLite database for testing.
    It initializes the app, creates the database tables, 
    and provides a test client for making HTTP requests.
    """
    app = create_app("testing")

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()

@pytest.fixture(name="new_user")
def new_user_fixture():
    """
    Fixture that creates a new user instance with predefined data.
    This fixture can be used to test user-related functionality.
    """
    return UserModel(name="Test User", email="testuser@example.com", password="password123")

@pytest.fixture(name="user_library_entry")
def user_library_entry_fixture():
    """
    Fixture that creates a new user library entry with predefined data.
    The entry associates a user with a book and assigns a reading status.
    """
    return UserLibraryModel(user_id=1, book_id=1, status="reading")


@pytest.fixture(name="app2")
def app2_fixture():
    """Create a Flask app instance for testing."""
    app2 = create_app("testing")
    with app2.app_context():
        db.create_all()
        yield app2
        db.session.remove()
        db.drop_all()

@pytest.fixture(name="test_client2")
def test_client2_fixture(app2):
    """Create a test client."""
    return app2.test_client()
