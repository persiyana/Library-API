"""
This module defines the `Register` resource for user registration.
It uses Flask-RESTful to handle API requests and SQLAlchemy for database interaction.

Modules:
    - reqparse (flask_restful): Used to parse incoming request data for user registration.
    - generate_password_hash (werkzeug.security): Used to securely hash the user's password.
    - db: SQLAlchemy instance used to interact with the database.
    - UserModel: Represents the user entity and interacts with the `users` table in the database.

Classes:
    - Register: A Flask-RESTful resource for registering a new user.

Methods:
    - post(): Handles the user registration process, including checking 
    for duplicate email and storing the new user in the database.
"""
from flask_restful import Resource, reqparse
from models import db
from models.user_model import UserModel

class Register(Resource):
    """
    Represents the resource for registering a new user. 
    Handles the registration of a user by accepting user details, verifying that 
    the email is unique, and saving the new user in the database.

    Methods:
        post(): Handles the user registration by accepting user details and storing the new user 
        in the database.
    """
    def post(self):
        """
        Handles the POST request to register a new user. 
        It checks if the email is already registered and stores the user in the database 
        if the email is unique.
        
        The function accepts the user's name, email, and password, and performs the necessary 
        validation to ensure that the email is not already registered. If the validation passes, 
        the user is added to the database with a hashed password.

        Returns:
            dict: A dictionary containing a message indicating success or failure 
            of the registration process.
            status_code (int): The corresponding HTTP status code indicating the result 
            of the operation.

        Error Responses:
            - 400: If the email is already registered.
        """
        args = reqparse.RequestParser()
        args.add_argument('name', type=str, required=True)
        args.add_argument('email', type=str, required=True)
        args.add_argument('password', type=str, required=True)
        data = args.parse_args()

        if UserModel.query.filter_by(email=data['email']).first():
            return {'message': 'Email already registered'}, 400

        user = UserModel(name=data['name'], email=data['email'], password=data['password'])
        db.session.add(user)
        db.session.commit()
        return {'message': 'User registered successfully'}, 201
