"""
This module defines the `UserModel` class, which represents a user in the database.
It is used to interact with the `users` table, allowing for user creation, password verification, 
and role-based authorization.

Modules:
    - db: The SQLAlchemy instance for interacting with the database.
    - werkzeug.security: Provides utilities for hashing and checking passwords.

Classes:
    - UserModel: Represents a user with attributes such as name, email, password, and role.

Methods:
    - __init__(name, email, password, role="user"): Initializes a new UserModel instance.
    - verify_password(password): Verifies if the provided password matches the stored password.
    - change_password(new_password): Changes the user's password to a new one and 
    updates the database.
"""
from werkzeug.security import generate_password_hash, check_password_hash
from models import db

class UserModel(db.Model):
    """
    Represents a user in the system with their details, such as name, email, password, and role.

    Attributes:
        id (int): The unique identifier of the user.
        name (str): The name of the user.
        email (str): The email address of the user.
        password (str): The hashed password of the user.
        role (str): The role of the user, such as "user" or "admin". Defaults to "user".

    Methods:
        __init__(name, email, password, role="user"): Initializes a new user instance 
        with provided details.
        verify_password(password): Verifies if the provided password matches 
        the stored password hash.
        change_password(new_password): Changes the password to a new value and updates it 
        in the database.
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(10), default="user")

    def __init__(self, name: str, email: str, password: str, role: str = "user"):
        """
        Initializes a new UserModel instance with the provided user details.

        Args:
            name (str): The name of the user.
            email (str): The email address of the user.
            password (str): The password provided by the user.
            role (str, optional): The role of the user (default is "user").
        """
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)
        self.role = role

    def verify_password(self, password: str) -> bool:
        """
        Verifies if the provided password matches the user's stored password.

        Args:
            password (str): The password to verify.

        Returns:
            bool: True if the provided password matches the stored password hash, False otherwise.
        """
        return check_password_hash(self.password, password)

    def change_password(self, new_password: str) -> None:
        """
        Changes the user's password to a new one and updates it in the database.

        Args:
            new_password (str): The new password to set for the user.
        
        Side Effects:
            - Updates the password in the database to the hashed new password.
        """
        self.password = generate_password_hash(new_password)
        db.session.commit()
