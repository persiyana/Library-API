"""
This module defines the `Register` resource for user registration.
It uses Flask-RESTful to handle API requests and SQLAlchemy for database interaction.
"""
from flask_restful import Resource, reqparse
from models import db
from models.user_model import UserModel

class Register(Resource):
    """
    Represents the resource for registering a new user. 
    Handles the registration of a user by accepting user details, verifying that 
    the email is unique, and saving the new user in the database.
    """
    def post(self):
        """
        Handles the POST request to register a new user. 
        It checks if the email is already registered and stores the user in the database 
        if the email is unique.
        
        The function accepts the user's name, email, and password, and performs the necessary 
        validation to ensure that the email is not already registered. If the validation passes, 
        the user is added to the database with a hashed password.
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
