"""
This module defines the `Books` resource for managing book-related operations like retrieval, 
creation, updating, and deletion. The resource is part of a Flask-RESTful API 
and uses JWT authentication.

Modules:
    - reqparse (flask_restful): Used to parse incoming request data for the different operations.
    - jwt_required, get_jwt_identity (flask_jwt_extended): Used for user authentication 
    and getting the current user's identity.
    - BookModel: Represents the book entity and interacts with the `books` table in the database.
    - UserModel: Represents the user entity, used for verifying the current user 
    and their permissions.
    - db: Provides SQLAlchemy database interaction.

Classes:
    - Books: A Flask-RESTful resource that handles CRUD operations for books.

Methods:
    - get(book_id=None): Retrieves a book or a list of books based on search criteria.
    - post(): Adds a new book to the database.
    - patch(book_id): Updates an existing book's information.
    - delete(book_id): Deletes a book from the database.
"""
from flask_restful import reqparse, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.book_model import BookModel
from models.user_model import UserModel
from models import db

class Books(Resource):
    """
    Represents the resource for handling book-related CRUD operations, including retrieval, 
    creation, updating, and deletion.

    Methods:
        get(book_id=None): Retrieves a specific book or a list of books based on search criteria.
        post(): Adds a new book to the database.
        patch(book_id): Updates the details of an existing book.
        delete(book_id): Deletes a book from the database.

    Args:
        book_id (int, optional): The ID of the book to retrieve, update, or delete.
    """
    @jwt_required()
    def get(self, book_id = None):
        """
        Handles the GET request to retrieve book(s). If a book ID is provided, 
        it retrieves the details of a specific book along with its reviews. 
        If no book ID is provided, it searches for books 
        based on the provided search criteria.

        Args:
            book_id (int, optional): The ID of the book to retrieve. Defaults to None.

        Returns:
            dict: A dictionary representing the book(s) and their details or an error message.
            status_code (int): The corresponding HTTP status code.

        Error Responses:
            - 404: If the book with the given ID is not found or no books match the search criteria.
        """
        book = BookModel.query.get(book_id)
        if book_id:
            book = BookModel.query.get(book_id)
            if not book:
                return {'message': 'Book not found'}, 404

            reviews = [{
                'user_name': review.user.name, 
                'rating': review.rating, 
                'review_text': review.review_text} for review in book.reviews]
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

        Returns:
            dict: A message indicating whether the book was added successfully 
            or if there was an error.
            status_code (int): The corresponding HTTP status code.

        Error Responses:
            - 403: If the user is not authenticated.
            - 400: If the book already exists in the database.
        """
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

        Args:
            book_id (int): The ID of the book to update.

        Returns:
            dict: A message indicating whether the book was updated successfully 
            or if there was an error.
            status_code (int): The corresponding HTTP status code.

        Error Responses:
            - 403: If the user is not authenticated or is not an admin.
            - 404: If the book with the given ID is not found.
        """
        current_user = get_jwt_identity()
        user_data = UserModel.query.get(current_user)

        if user_data is None or user_data.role != 'admin':
            return {'message': 'Unauthorized access'}, 403

        selected_book = BookModel.query.get(book_id)
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

        Args:
            book_id (int): The ID of the book to delete.

        Returns:
            dict: A message indicating whether the book was deleted successfully or 
            if there was an error.
            status_code (int): The corresponding HTTP status code.

        Error Responses:
            - 403: If the user is not authenticated or is not an admin.
            - 404: If the book with the given ID is not found.
        """
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
