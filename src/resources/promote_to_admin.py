"""
This module defines the `PromoteToAdmin` resource for promoting a user to the admin role.
It uses Flask-RESTful for API functionality and JWT for user authentication.
"""
from flask_restful import reqparse, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user_model import UserModel
from src.models import db

class PromoteToAdmin(Resource):
    """
    Represents the resource for promoting a user to the admin role. 
    The user requesting the promotion must be an admin.
    """

    @jwt_required()
    def post(self):
        """
        Handles the POST request to promote a user to the admin role. 
        It checks that the current user is an admin and that the user to be promoted exists.
        
        The function verifies that the current user has the `admin` role, and then searches 
        for the user specified by email. If found and not already an admin, the user's 
        role is updated to `admin`.
        """
        current_user_id = get_jwt_identity()
        current_user = db.session.get(UserModel, current_user_id)

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
