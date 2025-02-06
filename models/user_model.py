"""
This module defines the `UserModel` class, which represents a user in the database.
It is used to interact with the `users` table, allowing for user creation, password verification, 
and role-based authorization.
"""
from werkzeug.security import generate_password_hash, check_password_hash
from models import db

class UserModel(db.Model):
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
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)
        self.role = role

    def verify_password(self, password: str) -> bool:
        """
        Verifies if the provided password matches the user's stored password.
        """
        return check_password_hash(self.password, password)

    def change_password(self, new_password: str) -> None:
        """
        Changes the user's password to a new one and updates it in the database.
        """
        self.password = generate_password_hash(new_password)
        db.session.commit()
