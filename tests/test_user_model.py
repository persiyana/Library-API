"""
This module contains tests for user-related operations, including user creation,
password verification, and password change functionality.
"""
import pytest
from werkzeug.security import check_password_hash
from models import db
from models.user_model import UserModel
from main import create_app

@pytest.fixture(scope="module", name="test_client")
def test_client_fixture():
    """
    Fixture that sets up the Flask app and creates an in-memory database for testing.
    It initializes the application, configures the database, and provides a test client 
    for making requests to the app.

    The database is created at the start of the test and dropped after the tests complete.
    """
    app = create_app()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()

@pytest.fixture(name="new_user")
def new_user_fixture():
    """
    Fixture that creates a new user instance with predefined name, email, and password.
    This user instance is used in various tests to simulate user creation and authentication.
    """
    return UserModel(name="TestUser", email="testuser@example.com", password="password123")

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
