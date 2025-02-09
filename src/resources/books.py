"""
This module defines the `Books` resource for managing book-related operations like retrieval, 
creation, updating, and deletion. The resource is part of a Flask-RESTful API 
and uses JWT authentication.
"""
from flask_restful import reqparse, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.book_model import BookModel
from src.models.user_model import UserModel
from src.models.user_library_model import UserLibraryModel
from src.models import db

class Books(Resource):
    """
    Represents the resource for handling book-related CRUD operations, including retrieval, 
    creation, updating, and deletion.
    """
    @jwt_required()
    def get(self, book_id = None):
        """
        Handles the GET request to retrieve book(s). If a book ID is provided, 
        it retrieves the details of a specific book along with its reviews. 
        If no book ID is provided, it searches for books 
        based on the provided search criteria.
        """
        if book_id:
            book = db.session.get(BookModel, book_id)
            if not book:
                return {'message': 'Book not found'}, 404

            reviews = [{
                'user_name': review.user.name, 
                'rating': review.rating, 
                'review_text': review.review_text} for review in book.reviews.all()]
            return {
                'id': book.id,
                'title': book.title,
                'author': book.author,
                'genre': book.genre,
                'description': book.description,
                'average_rating': book.average_rating,
                'reviews': reviews
            }, 200

        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str)
        parser.add_argument('author', type=str)
        parser.add_argument('genre', type=str)
        args = parser.parse_args()

        books = BookModel.search_books(args['title'], args['author'], args['genre'])

        if not books:
            return {'message': 'No books found matching the search criteria'}, 404

        return [{'id': book.id, 'title': book.title, 'author': book.author, 'genre': book.genre}
                for book in books], 200

    @jwt_required()
    def post(self):
        """
        Handles the POST request to add a new book to the database. 
        The user must be authenticated to create a book. 
        It validates the book's details and ensures the book doesn't already exist.
        """
        current_user_id = get_jwt_identity()
        user = db.session.get(UserModel, current_user_id)

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

        new_book = BookModel({
            'title': data['title'],
            'author': data['author'],
            'genre': data['genre'],
            'description': data.get('description', '')}
        )

        db.session.add(new_book)
        db.session.commit()

        return {'message': 'Book added successfully'}, 201

    @jwt_required()
    def patch(self, book_id):
        """
        Handles the PATCH request to update an existing book's details. The user must be an admin to 
        perform this action.
        """
        current_user = get_jwt_identity()
        user_data = db.session.get(UserModel, current_user)

        if user_data is None or user_data.role != 'admin':
            return {'message': 'Unauthorized access'}, 403

        selected_book = db.session.get(BookModel, book_id)
        if selected_book is None:
            return {'message': 'No matching book found'}, 404

        args = reqparse.RequestParser()
        args.add_argument('title', type=str)
        args.add_argument('author', type=str)
        args.add_argument('genre', type=str)
        args.add_argument('description', type=str)
        data = args.parse_args()

        if data['title']:
            selected_book.title = data['title']
        if data['author']:
            selected_book.author = data['author']
        if data['genre']:
            selected_book.genre = data['genre']
        if data['description']:
            selected_book.description = data['description']

        db.session.commit()
        return {'message': 'Book updated successfully'}

    @jwt_required()
    def delete(self, book_id):
        """
        Handles the DELETE request to remove a book from the database. The user must be an admin to 
        perform this action.
        """
        current_user_id = get_jwt_identity()
        user = db.session.get(UserModel, current_user_id)

        if not user or user.role != 'admin':
            return {'message': 'Unauthorized'}, 403

        book = db.session.get(BookModel, book_id)
        if not book:
            return {'message': 'Book not found'}, 404

        user_libraries = UserLibraryModel.query.filter_by(book_id=book.id).all()
        for user_library in user_libraries:
            db.session.delete(user_library)

        db.session.delete(book)
        db.session.commit()
        return {'message': 'Book deleted successfully'}
