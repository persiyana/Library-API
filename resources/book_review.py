"""
This module defines the `BookReview` resource, 
which allows users to submit reviews for a specific book.
"""
from flask_restful import reqparse, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user_model import UserModel
from models.review_model import ReviewModel
from models.book_model import BookModel
from models import db
class BookReview(Resource):
    """
    Represents the resource for submitting a review for a specific book.
    """
    @jwt_required()
    def post(self, book_id):
        """
        Handles the POST request to submit a review for a book.

        This method allows an authenticated user to submit a review for a specific book. 
        It checks the validity of the rating, ensures the user hasn't already reviewed 
        the book, and updates the average rating of the book based on the new review.
        """

        current_user_id = get_jwt_identity()
        user = db.session.get(UserModel, current_user_id)

        if not user:
            return {'message': 'Unauthorized'}, 403

        book = db.session.get(BookModel, book_id)
        if not book:
            return {'message': 'Book not found'}, 404

        args = reqparse.RequestParser()
        args.add_argument('rating', type=int, required=True, help='Rating is required (1-5)')
        args.add_argument('review_text', type=str, required=False)
        data = args.parse_args()

        if data['rating'] < 1 or data['rating'] > 5:
            return {'message': 'Rating must be between 1 and 5'}, 400

        existing_review = ReviewModel.query.filter_by(user_id=current_user_id,
                                                      book_id=book_id).first()
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
