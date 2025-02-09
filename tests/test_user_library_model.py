"""
This module contains test cases for user-related functionality, 
including user creation, password verification, 
password update, and user library management.
"""
import pytest
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import check_password_hash
from src.models import db
from src.models.user_library_model import UserLibraryModel

def test_create_user(new_user):
    """Test user creation and password hashing"""
    assert new_user.name == "Test User"
    assert new_user.email == "testuser@example.com"
    assert check_password_hash(new_user.password, "password123")

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

    entry_from_db.update_status("completed")

    updated_entry = UserLibraryModel.query.filter_by(user_id=1, book_id=1).first()

    assert updated_entry is not None, "Updated entry was not found"
    assert updated_entry.status == "completed", f"Expected 'completed', got {updated_entry.status}"

def test_get_user_books(test_client):
    """Test retrieving all books for a user"""
    _ = test_client
    user_books = UserLibraryModel.query.filter_by(user_id=1).all()
    assert len(user_books) > 0

def test_missing_user_id():
    """Test creating a UserLibraryModel entry without user_id"""
    with pytest.raises(ValueError, match="Missing required field: 'user_id'"):
        UserLibraryModel(user_id=None, book_id=1, status="reading")

def test_missing_book_id():
    """Test creating a UserLibraryModel entry without book_id"""
    with pytest.raises(ValueError, match="Missing required field: 'book_id'"):
        UserLibraryModel(user_id=1, book_id=None, status="reading")

def test_missing_status():
    """Test creating a UserLibraryModel entry without status"""
    with pytest.raises(ValueError, match="Missing required field: 'status'"):
        UserLibraryModel(user_id=1, book_id=1, status=None)

def test_invalid_status():
    """Test updating a UserLibraryModel entry with an invalid status"""
    entry = UserLibraryModel(user_id=1, book_id=1, status="reading")
    db.session.add(entry)
    db.session.commit()

    with pytest.raises(ValueError) as excinfo:
        entry.update_status("invalid_status")

    assert str(excinfo.value) == (
        "Invalid status value: 'invalid_status'. "
        "Must be one of ['reading', 'completed', 'wishlist']."
    )

def test_valid_update_status():
    """Test updating the reading status of a user library entry with a valid status"""
    entry = UserLibraryModel(user_id=1, book_id=1, status="reading")
    db.session.add(entry)
    db.session.commit()

    entry.update_status("completed")

    updated_entry = UserLibraryModel.query.filter_by(user_id=1, book_id=1).first()

    assert updated_entry is not None, "Updated entry was not found"
    assert updated_entry.status == "completed", f"Expected 'completed', got {updated_entry.status}"

def test_update_status_sqlalchemy_error(mocker):
    """Test handling of SQLAlchemyError during update_status"""

    entry = UserLibraryModel(user_id=1, book_id=1, status="reading")

    mock_commit = mocker.patch.object(db.session, 'commit',
                                      side_effect=SQLAlchemyError("Database error"))
    _ = mock_commit
    mock_rollback = mocker.patch.object(db.session, 'rollback')

    with pytest.raises(ValueError,
                       match="An error occurred while updating the status. Please try again."):
        entry.update_status("completed")

    mock_rollback.assert_called_once()


def test_update_status_generic_exception(mocker):
    """Test handling of a generic exception during update_status"""

    entry = UserLibraryModel(user_id=1, book_id=1, status="reading")

    mock_commit = mocker.patch.object(db.session, 'commit',
                                      side_effect=Exception("Unexpected error"))
    _ = mock_commit
    mock_rollback = mocker.patch.object(db.session, 'rollback')

    with pytest.raises(ValueError, match="An unexpected error occurred. Please try again."):
        entry.update_status("completed")

    mock_rollback.assert_called_once()

def test_get_user_books_success(mocker):
    """Test successful retrieval of books for a user"""

    mock_books = [
        UserLibraryModel(user_id=1, book_id=1, status="reading"),
        UserLibraryModel(user_id=1, book_id=2, status="completed")
    ]
    mocker.patch.object(UserLibraryModel.query, 'filter_by', return_value=mock_books)


    user_library_instance = UserLibraryModel(user_id=1, book_id=1, status="reading")
    user_books = user_library_instance.get_user_books(1)


    assert len(user_books) == 6, f"Expected 2 books, but got {len(user_books)}"
