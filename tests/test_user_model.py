"""
This module contains tests for user-related operations, including user creation,
password verification, and password change functionality.
"""
from models import db
from models.user_model import UserModel

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
