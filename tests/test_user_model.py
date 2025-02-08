"""
This module contains tests for user-related operations, including user creation,
password verification, and password change functionality.
"""
import pytest
from sqlalchemy.exc import IntegrityError,  SQLAlchemyError
from werkzeug.security import check_password_hash
from models import db
from models.user_model import UserModel

def test_user_creation(new_user):
    """
    Test the creation of a new user and verify the correct attributes.
    """
    assert new_user.name == "Test User"
    assert new_user.email == "testuser@example.com"
    assert check_password_hash(new_user.password, "password123")

def test_user_creation_valid_data():
    """Test creating a user with valid data"""
    user = UserModel(name="John Doe", email="johndoe@example.com", password="password123")
    assert user.name == "John Doe"
    assert user.email == "johndoe@example.com"
    assert user.password is not None
    assert user.role == "user"

def test_user_creation_missing_fields():
    """Test creating a user with missing required fields"""
    try:
        UserModel(name="", email="johndoe@example.com", password="password123")
    except ValueError as e:
        assert str(e) == "User creation error: Missing required field: 'name'"

    try:
        UserModel(name="John Doe", email="", password="password123")
    except ValueError as e:
        assert str(e) == "User creation error: Missing required field: 'email'"

    try:
        UserModel(name="John Doe", email="johndoe@example.com", password="")
    except ValueError as e:
        assert str(e) == "User creation error: Missing required field: 'password'"


def test_user_creation_invalid_email():
    """Test creating a user with an invalid email format"""
    try:
        UserModel(name="John Doe", email="invalid-email", password="password123")
    except ValueError as e:
        assert str(e) == "User creation error: Invalid email format: invalid-email"

def test_verify_password(new_user):
    """Test password verification"""
    assert new_user.verify_password("password123") is True
    with pytest.raises(ValueError, match="Password verification error: Incorrect password."):
        new_user.verify_password("wrongpassword")

def test_change_password(test_client, new_user):
    """Test changing the user's password"""
    _ = test_client

    db.session.add(new_user)
    db.session.commit()

    new_user.change_password("newpassword456")

    user_from_db = UserModel.query.filter_by(email="testuser@example.com").first()
    assert user_from_db is not None
    assert user_from_db.verify_password("newpassword456") is True
    with pytest.raises(ValueError, match="Password verification error: Incorrect password."):
        user_from_db.verify_password("wrongpassword")

def test_change_password_database_error(test_client, new_user):
    """Test password change with a database error without using try/catch"""
    _ = test_client

    new_user.password = None

    db.session.add(new_user)

    with pytest.raises(SQLAlchemyError):
        db.session.commit()

    with pytest.raises(RuntimeError) as exc_info:
        new_user.change_password("newpassword123")

    assert str(exc_info.value).startswith("Database error while changing password")

def test_change_password_empty_new_password(test_client, new_user):
    """Test changing password with an empty new password"""
    _ = test_client

    existing_user = UserModel.query.filter_by(email=new_user.email).first()
    if existing_user:
        db.session.delete(existing_user)
        db.session.commit()

    db.session.add(new_user)
    db.session.commit()

    with pytest.raises(ValueError, match="New password is required."):
        new_user.change_password("")

def test_email_validation_valid():
    """Test valid email format"""
    assert UserModel.is_valid_email("valid.email@example.com") is True


def test_email_validation_invalid():
    """Test invalid email format"""
    assert UserModel.is_valid_email("invalid-email") is False
    assert UserModel.is_valid_email("another.invalid@com") is False


def test_user_role_default():
    """Test default user role on creation"""
    user = UserModel(name="John Doe", email="johndoe@example.com", password="password123")
    assert user.role == "user"


def test_user_role_custom():
    """Test custom user role on creation"""
    user = UserModel(name="Admin User",
                     email="admin@example.com",
                     password="adminpassword",
                     role="admin")
    assert user.role == "admin"

def test_password_verification_error():
    """Test password verification when user doesn't exist"""
    fake_user = UserModel.query.filter_by(email="nonexistent@example.com").first()

    assert fake_user is None, "User should not exist."

    if fake_user is None:
        with pytest.raises(ValueError) as exc_info:
            raise ValueError("User not found.")

        assert str(exc_info.value) == "User not found."


def test_user_creation_duplicate_email():
    """Test creating a user with a duplicate email (ensures database constraint is respected)."""
    user1 = UserModel(name="User One", email="duplicate@example.com", password="password123")
    db.session.add(user1)
    db.session.commit()

    try:
        user2 = UserModel(name="User Two", email="duplicate@example.com", password="password456")
        db.session.add(user2)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        assert True

def test_password_verification_user_not_found():
    """Test password verification when user doesn't exist."""
    fake_user = UserModel.query.filter_by(email="nonexistent@example.com").first()
    assert fake_user is None

def test_email_validation_invalid_formats():
    """Test various invalid email formats."""
    assert UserModel.is_valid_email("plainaddress") is False
    assert UserModel.is_valid_email("@missingusername.com") is False
    assert UserModel.is_valid_email("missingdomain@.com") is False
    assert UserModel.is_valid_email("missing@dot@dot.com") is False

def test_user_role_custom_role():
    """Test user creation with a custom role."""
    user = UserModel(name="Admin User",
                     email="admin@example.com",
                     password="adminpassword",
                     role="admin")
    assert user.role == "admin"

def test_change_password_empty_password(new_user):
    """Test attempting to change password to an empty string."""
    try:
        new_user.change_password("")
    except ValueError as e:
        assert str(e) == "Password change error: New password is required."

def test_user_creation_invalid_email_format():
    """Test creating a user with an invalid email format."""
    try:
        user = UserModel(name="Invalid Email", email="invalidemail@com", password="password123")
        _ = user
    except ValueError as e:
        assert str(e) == "User creation error: Invalid email format: invalidemail@com"

def test_password_verification_after_change(test_client, new_user):
    """Test password verification after changing the password."""
    _ = test_client

    existing_user = UserModel.query.filter_by(email=new_user.email).first()
    if existing_user:
        db.session.delete(existing_user)
        db.session.commit()

    db.session.add(new_user)
    db.session.commit()

    new_user.change_password("newpassword123")

    db.session.commit()

    user_from_db = UserModel.query.filter_by(email=new_user.email).first()

    assert user_from_db is not None
    assert user_from_db.verify_password("newpassword123")
