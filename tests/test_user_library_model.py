"""
This module contains test cases for user-related functionality, 
including user creation, password verification, 
password update, and user library management.
"""
from werkzeug.security import check_password_hash
from models import db
from models.user_library_model import UserLibraryModel

def test_create_user(new_user):
    """Test user creation and password hashing"""
    assert new_user.name == "TestUser"
    assert new_user.email == "testuser@example.com"
    assert check_password_hash(new_user.password, "password123")


def test_verify_password(new_user):
    """Test password verification"""
    assert new_user.verify_password("password123") is True
    assert new_user.verify_password("wrongpassword") is False

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
