from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user_library_model import UserLibraryModel
from models.user_model import UserModel
from models.review_model import ReviewModel

class UserProfile(Resource):
    @jwt_required()
    def get(self):
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
            'library': [{'book_id': entry.book_id, 'status': entry.status} for entry in user_library],
            'reviews': [{'book_id': review.book_id, 'rating': review.rating, 'review_text': review.review_text} for review in user_reviews]
        }, 200