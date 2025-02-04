from flask_restful import reqparse, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.book_model import BookModel
from models.user_model import UserModel
from extensions import db

class Books(Resource):
    @jwt_required()
    def get(self, book_id):
        book = BookModel.query.get(book_id)
        if not book:
            return {'message': 'Book not found'}, 404

        reviews = [{'user_name': review.user.name, 'rating': review.rating, 'review_text': review.review_text} for review in book.reviews]
        return {
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'genre': book.genre,
            'description': book.description,
            'average_rating': book.average_rating,
            'reviews' : reviews
        }, 200

    @jwt_required() 
    def post(self):
        current_user_id = get_jwt_identity()
        user = UserModel.query.get(current_user_id)

        if not user: 
            return {'message': 'Unauthorized'}, 403

        args = reqparse.RequestParser()
        args.add_argument('title', type=str, required=True)
        args.add_argument('author', type=str, required=True)
        args.add_argument('genre', type=str, required=True)
        args.add_argument('description', type=str, required=False)
        data = args.parse_args()

        if BookModel.query.filter_by(title=data['title'], author=data['author']).first():
            return {'message': 'Book already exists'}, 400

        new_book = BookModel(
            title=data['title'],
            author=data['author'],
            genre=data['genre'],
            description=data.get('description', '')
        )

        db.session.add(new_book)
        db.session.commit()

        return {'message': 'Book added successfully'}, 201
    
    @jwt_required()
    def patch(self, book_id):
        current_user_id = get_jwt_identity()
        user = UserModel.query.get(current_user_id)

        if not user or user.role != 'admin':
            return {'message': 'Unauthorized'}, 403

        book = BookModel.query.get(book_id)
        if not book:
            return {'message': 'Book not found'}, 404

        args = reqparse.RequestParser()
        args.add_argument('title', type=str)
        args.add_argument('author', type=str)
        args.add_argument('genre', type=str)
        args.add_argument('description', type=str)
        data = args.parse_args()

        if data['title']:
            book.title = data['title']
        if data['author']:
            book.author = data['author']
        if data['genre']:
            book.genre = data['genre']
        if data['description']:
            book.description = data['description']

        db.session.commit()
        return {'message': 'Book updated successfully'}

    @jwt_required()
    def delete(self, book_id):
        current_user_id = get_jwt_identity()
        user = UserModel.query.get(current_user_id)

        if not user or user.role != 'admin':
            return {'message': 'Unauthorized'}, 403

        book = BookModel.query.get(book_id)
        if not book:
            return {'message': 'Book not found'}, 404

        db.session.delete(book)
        db.session.commit()
        return {'message': 'Book deleted successfully'}