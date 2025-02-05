"""
This module defines the `Login` resource for handling user authentication via login. 
It uses Flask-RESTful for API functionality and JWT for user session management.

Modules:
    - reqparse (flask_restful): Used to parse incoming request data for login.
    - create_access_token (flask_jwt_extended): Used to generate an access token for the user.
    - check_password_hash (werkzeug.security): Used to verify the provided password against 
    the stored hash.
    - UserModel: Represents the user entity and interacts with the `users` table in the database.

Classes:
    - Login: A Flask-RESTful resource that handles user login and returns an access token.

Methods:
    - post(): Authenticates the user by verifying the provided email and password, 
    and generates an access token.
"""
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from models.user_model import UserModel

class Login(Resource):
    """
    Represents the login resource for authenticating users and generating JWT access tokens.

    Methods:
        post(): Handles user login by verifying the email and password and returning 
        an access token.
    """
    def post(self):
        """
        Handles the POST request to authenticate a user. It checks whether the provided email 
        exists in the database, and if so, compares the provided password with
        the stored password hash. 
        If authentication is successful, an access token is generated and returned.

        Returns:
            dict: A dictionary containing the `access_token` if authentication is successful, or 
                  an error message if authentication fails.
            status_code (int): The corresponding HTTP status code.

        Error Responses:
            - 401: If the user is not found or the provided password is incorrect.
        """
        args = reqparse.RequestParser()
        args.add_argument('email', type=str, required=True)
        args.add_argument('password', type=str, required=True)
        data = args.parse_args()

        user = UserModel.query.filter_by(email=data['email']).first()
        if not user:
            return {'message': 'Invalid user'}, 401

        if not check_password_hash(user.password, data['password']):
            return {'message': 'Invalid pass'}, 401

        access_token = create_access_token(identity=user.id)
        return {'access_token': access_token}, 200
