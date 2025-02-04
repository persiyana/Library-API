from flask_restful import reqparse, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user_model import UserModel
from models.review_model import ReviewModel
from models.book_model import BookModel
from models import db

class BookReview(Resource):
    @jwt_required()
    def post(self, book_id):
        current_user_id = get_jwt_identity()
        user = UserModel.query.get(current_user_id)

        if not user:
            return {'message': 'Unauthorized'}, 403

        book = BookModel.query.get(book_id)
        if not book:
            return {'message': 'Book not found'}, 404

        args = reqparse.RequestParser()
        args.add_argument('rating', type=int, required=True, help='Rating is required (1-5)')
        args.add_argument('review_text', type=str, required=False)
        data = args.parse_args()

        if data['rating'] < 1 or data['rating'] > 5:
            return {'message': 'Rating must be between 1 and 5'}, 400

        existing_review = ReviewModel.query.filter_by(user_id=current_user_id, book_id=book_id).first()
        if existing_review:
            return {'message': 'You have already reviewed this book'}, 400


        review = ReviewModel(
            user_id=current_user_id,
            book_id=book_id,
            rating=data['rating'],
            review_text=data.get('review_text', '')
        )
        db.session.add(review)
        db.session.commit()

        book.update_average_rating()

        return {'message': 'Review added successfully'}, 201