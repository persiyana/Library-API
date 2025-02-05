"""
This module defines the `PromoteToAdmin` resource for promoting a user to the admin role.
It uses Flask-RESTful for API functionality and JWT for user authentication.

Modules:
    - reqparse (flask_restful): Used to parse incoming request data for promoting a user.
    - jwt_required, get_jwt_identity (flask_jwt_extended): Used to ensure the request 
    is authenticated and get the current user's identity.
    - UserModel: Represents the user entity and interacts with the `users` table in the database.
    - db: SQLAlchemy instance used to interact with the database.

Classes:
    - PromoteToAdmin: A Flask-RESTful resource for promoting a user to the admin role.

Methods:
    - post(): Promotes a user to the admin role if the current user is an admin and the user exists.
"""
from flask_restful import reqparse, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user_model import UserModel
from models import db

class PromoteToAdmin(Resource):
    """
    Represents the resource for promoting a user to the admin role. 
    The user requesting the promotion must be an admin.

    Methods:
        post(): Handles the promotion of a user to the admin role.
    """

    @jwt_required()
    def post(self):
        """
        Handles the POST request to promote a user to the admin role. 
        It checks that the current user is an admin and that the user to be promoted exists.
        
        The function verifies that the current user has the `admin` role, and then searches 
        for the user specified by email. If found and not already an admin, the user's 
        role is updated to `admin`.

        Returns:
            dict: A dictionary containing a message indicating success or failure 
            of the promotion process.
            status_code (int): The corresponding HTTP status code indicating the result 
            of the operation.

        Error Responses:
            - 403: If the current user is not an admin.
            - 404: If the user to promote is not found.
            - 400: If the user to promote is already an admin.
        """
        current_user_id = get_jwt_identity()
        current_user = UserModel.query.get(current_user_id)

        assert isinstance(current_user, UserModel), "User must be an instance of UserModel"

        if current_user.role != 'admin':
            return {'message': 'You must be an admin to perform this action'}, 403

        args = reqparse.RequestParser()
        args.add_argument('email', type=str, required=True, help='Email of the user to promote')
        data = args.parse_args()

        user_to_promote = UserModel.query.filter_by(email=data['email']).first()

        if not user_to_promote:
            return {'message': 'User not found'}, 404

        if user_to_promote.role == 'admin':
            return {'message': 'This user is already an admin'}, 400

        user_to_promote.role = 'admin'
        db.session.commit()

        return {'message': f'User {data["email"]} has been promoted to admin'}, 200
