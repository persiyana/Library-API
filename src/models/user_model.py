"""
This module defines the `UserModel` class, which represents a user in the database.
It is used to interact with the `users` table, allowing for user creation, password verification, 
and role-based authorization.
"""
import re
from typing import TYPE_CHECKING
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import SQLAlchemyError
from src.models import db
from src.utils.validators import validate_required_fields

if TYPE_CHECKING:
    from flask_sqlalchemy.model import Model
else:
    Model = db.Model

class UserModel(Model):
    """
    Represents a user in the system with their details, such as name, email, password, and role.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(10), default="user")

    def __init__(self, name: str, email: str, password: str, role: str = "user"):
        """
        Initializes a new UserModel instance with the provided user details.
        """
        try:
            validate_required_fields(name = name, email = email, password = password)
            self.name = name
            self.email = email

            if not self.is_valid_email(email):
                raise ValueError(f"Invalid email format: {email}")

            self.password = generate_password_hash(password)
            self.role = role
        except ValueError as e:
            raise ValueError(f"User creation error: {str(e)}") from e

    def verify_password(self, password: str) -> bool:
        """
        Verifies if the provided password matches the user's stored password.
        """
        try:
            if not check_password_hash(self.password, password):
                raise ValueError("Incorrect password.")
            return True
        except ValueError as e:
            raise ValueError(f"Password verification error: {str(e)}") from e

    def change_password(self, new_password: str) -> None:
        """
        Changes the user's password to a new one and updates it in the database.
        """
        try:
            if not new_password:
                raise ValueError("New password is required.")

            self.password = generate_password_hash(new_password)
            db.session.commit()
        except ValueError as e:
            raise ValueError(f"Password change error: {str(e)}") from e
        except SQLAlchemyError as e:
            db.session.rollback()
            raise RuntimeError(f"Database error while changing password: {str(e)}") from e

    @staticmethod
    def is_valid_email(email: str) -> bool:
        """
        Validates the email format using a simple regex.
        """
        email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        return re.match(email_regex, email) is not None
