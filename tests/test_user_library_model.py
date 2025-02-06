"""
This module contains test cases for user-related functionality, 
including user creation, password verification, 
password update, and user library management.
"""
import pytest
from werkzeug.security import check_password_hash
from models import db
from models.user_model import UserModel
from models.user_library_model import UserLibraryModel
from main import create_app

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
    return UserModel(name="TestUser", email="testuser@example.com", password="password123")

@pytest.fixture(name="user_library_entry")
def user_library_entry_fixture():
    """
    Fixture that creates a new user library entry with predefined data.
    The entry associates a user with a book and assigns a reading status.
    """
    return UserLibraryModel(user_id=1, book_id=1, status="reading")

def test_create_user(new_user):
    """Test user creation and password hashing"""
    assert new_user.name == "TestUser"
    assert new_user.email == "testuser@example.com"
    assert check_password_hash(new_user.password, "password123")


def test_verify_password(new_user):
    """Test password verification"""
    assert new_user.verify_password("password123") is True
    assert new_user.verify_password("wrongpassword") is False


def test_change_password(test_client, new_user):
    """Test changing the user's password"""
    _ = test_client
    db.session.add(new_user)
    db.session.commit()

    new_user.change_password("newpassword456")

    user_from_db = UserModel.query.filter_by(email="testuser@example.com").first()
    assert user_from_db is not None
    assert user_from_db.verify_password("newpassword456") is True
    assert user_from_db.verify_password("password123") is False

def test_create_user_library_entry(test_client, user_library_entry):
    """Test creating a user library entry"""
    _ = test_client
    db.session.add(user_library_entry)
    db.session.commit()

    entry_from_db = UserLibraryModel.query.filter_by(user_id=1, book_id=1).first()
    assert entry_from_db is not None
    assert entry_from_db.status == "reading"

def test_update_library_status(test_client):
    """Test updating the reading status of a user library entry"""
    _ = test_client
    entry = UserLibraryModel(user_id=1, book_id=1, status="reading")
    db.session.add(entry)
    db.session.commit()

    entry_from_db = UserLibraryModel.query.filter_by(user_id=1, book_id=1).first()
    assert entry_from_db is not None, "Expected a database entry but found None"
    assert entry_from_db.status == "reading", f"Expected 'reading', got {entry_from_db.status}"

    entry_from_db.update_status("finished")

    updated_entry = UserLibraryModel.query.filter_by(user_id=1, book_id=1).first()

    assert updated_entry is not None, "Updated entry was not found"
    assert updated_entry.status == "finished", f"Expected 'finished', got {updated_entry.status}"

def test_get_user_books(test_client):
    """Test retrieving all books for a user"""
    _ = test_client
    user_books = UserLibraryModel.query.filter_by(user_id=1).all()
    assert len(user_books) > 0
