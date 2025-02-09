"""
This module defines the `UserProfile` resource, which allows users to retrieve 
information about their profile, including their library and reviews.
"""
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user_library_model import UserLibraryModel
from src.models.user_model import UserModel
from src.models.review_model import ReviewModel

class UserProfile(Resource):
    """
    Represents the resource for managing the user's profile.
    """
    @jwt_required()
    def get(self):
        """
        Handles the GET request to retrieve the current user's profile.
        
        The method fetches the user's details (ID, name, email, and role), 
        as well as their books in the library and the reviews they have written.
        """
        current_user_id = get_jwt_identity()
        user = UserModel.query.get(current_user_id)
        if not user:
            return {'message': 'User not found'}, 404

        user_library = UserLibraryModel.query.filter_by(user_id=current_user_id).all()
        user_reviews = ReviewModel.query.filter_by(user_id=current_user_id).all()
        return {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'role': user.role,
            'library': [{'book_id': entry.book_id,
                         'status': entry.status} for entry in user_library],
            'reviews': [{'book_id': review.book_id,
                         'rating': review.rating,
                         'review_text': review.review_text} for review in user_reviews]
        }, 200
