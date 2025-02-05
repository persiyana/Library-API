"""
This module defines the `UserLibrary` resource for managing a user's library.
It allows users to add, update, retrieve, and delete books in their personal library.

Modules:
    - reqparse (flask_restful): Used to parse incoming request data for user library actions.
    - jwt_required, get_jwt_identity (flask_jwt_extended): Used to enforce authentication 
    and retrieve the current user's identity.
    - db: SQLAlchemy instance used to interact with the database.
    - UserLibraryModel: Represents the `user_library` entity that holds books and their 
    status for each user.

Classes:
    - UserLibrary: A Flask-RESTful resource for managing the user's book library.

Methods:
    - get(): Retrieves all books from the user's library, categorized by their reading status.
    - post(): Adds a new book to the user's library with a specified status.
    - patch(): Updates the status of a book in the user's library.
    - delete(): Removes a book from the user's library.
"""
from flask_restful import reqparse, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user_library_model import UserLibraryModel
from models import db

class UserLibrary(Resource):
    """
    Represents the resource for managing the user's book library. 
    It provides the ability to retrieve, add, update, and delete books in the library, 
    based on their status.

    Methods:
        - get(): Retrieves all books in the user's library, categorized by their 
        status (read, reading, want to read).
        - post(): Adds a new book to the user's library with a specified status.
        - patch(): Updates the status of a specific book in the user's library.
        - delete(): Removes a book from the user's library.
    """
    @jwt_required()
    def get(self):
        """
        Handles the GET request to retrieve all books from the user's library.
        It categorizes the books into three statuses: 'read', 'currently reading', 
        and 'want to read'.
        
        Returns:
            dict: A dictionary containing lists of books under the three statuses.
            status_code (int): The HTTP status code, which is 200 for successful retrieval.
        
        Error Responses:
            - 401: If the user is not authenticated.
        """
        current_user_id = get_jwt_identity()

        read_books = UserLibraryModel.query.filter_by(user_id=current_user_id,
                                                      status="Прочетени").all()
        reading_books = UserLibraryModel.query.filter_by(user_id=current_user_id,
                                                         status="Чета в момента").all()
        want_to_read_books = UserLibraryModel.query.filter_by(user_id=current_user_id,
                                                              status="Искам да прочета").all()

        return {
            'read_books': [{
                'book_id': entry.book_id,
                'title': entry.book.title} for entry in read_books],
            'reading_books': [{
                'book_id': entry.book_id,
                'title': entry.book.title} for entry in reading_books],
            'want_to_read_books': [{
                'book_id': entry.book_id,
                'title': entry.book.title} for entry in want_to_read_books]
        }, 200

    @jwt_required()
    def post(self):
        """
        Handles the POST request to add a new book to the user's library with a specified status.
        
        The method checks if the status is valid and if the book is already in the user's library.
        If valid, it creates a new entry in the `user_library` table.
        
        Args:
            book_id (int): The ID of the book to add.
            status (str): The status of the book 
            ('Прочетени', 'Чета в момента', 'Искам да прочета').

        Returns:
            dict: A dictionary containing a success message indicating the book's status.
            status_code (int): The HTTP status code, which is 201 if successful.
        
        Error Responses:
            - 400: If the book's status is invalid or the book is already in the library.
            - 401: If the user is not authenticated.
        """
        current_user_id = get_jwt_identity()
        args = reqparse.RequestParser()
        args.add_argument('book_id', type=int, required=True, help='Book ID is required')
        args.add_argument('status', type=str, required=True,
                          help='Status (Прочетени, Чета в момента, Искам да прочета)')
        data = args.parse_args()

        if data['status'] not in ["Прочетени", "Чета в момента", "Искам да прочета"]:
            return {'message': 'Invalid status'}, 400

        existing_entry = UserLibraryModel.query.filter_by(user_id=current_user_id,
                                                          book_id=data['book_id']).first()
        if existing_entry:
            return {'message': 'Book already in your library'}, 400

        user_library_entry = UserLibraryModel(
            user_id=current_user_id,
            book_id=data['book_id'],
            status=data['status']
        )
        db.session.add(user_library_entry)
        db.session.commit()

        return {'message': f'Book added to library with status {data["status"]}'}, 201

    @jwt_required()
    def patch(self):
        """
        Handles the PATCH request to update the status of a book in the user's library.
        
        The method checks if the book exists in the library and if the new status is valid.
        If valid, it updates the book's status.
        
        Args:
            book_id (int): The ID of the book to update.
            new_status (str): The new status of the book 
            ('Прочетени', 'Чета в момента', 'Искам да прочета').

        Returns:
            dict: A dictionary containing a success message indicating the updated status.
            status_code (int): The HTTP status code, which is 200 if successful.
        
        Error Responses:
            - 400: If the new status is invalid.
            - 404: If the book is not found in the user's library.
            - 401: If the user is not authenticated.
        """
        current_user_id = get_jwt_identity()
        args = reqparse.RequestParser()
        args.add_argument('book_id', type=int, required=True, help='Book ID is required')
        args.add_argument('new_status', type=str, required=True,
                          help='New status (Прочетени, Чета в момента, Искам да прочета)')
        data = args.parse_args()

        if data['new_status'] not in ["Прочетени", "Чета в момента", "Искам да прочета"]:
            return {'message': 'Invalid status'}, 400

        user_library_entry = UserLibraryModel.query.filter_by(user_id=current_user_id,
                                                              book_id=data['book_id']).first()
        if not user_library_entry:
            return {'message': 'Book not found in your library'}, 404

        user_library_entry.status = data['new_status']
        db.session.commit()

        return {'message': f'Book status updated to {data["new_status"]}'}, 200

    @jwt_required()
    def delete(self):
        """
        Handles the DELETE request to remove a book from the user's library.
        
        The method checks if the book exists in the library. If it does, the book is deleted.
        
        Args:
            book_id (int): The ID of the book to remove from the library.

        Returns:
            dict: A dictionary containing a success message indicating the book has been removed.
            status_code (int): The HTTP status code, which is 200 if successful.
        
        Error Responses:
            - 404: If the book is not found in the user's library.
            - 401: If the user is not authenticated.
        """
        current_user_id = get_jwt_identity()
        args = reqparse.RequestParser()
        args.add_argument('book_id', type=int, required=True, help='Book ID is required')
        data = args.parse_args()

        user_library_entry = UserLibraryModel.query.filter_by(user_id=current_user_id,
                                                              book_id=data['book_id']).first()

        if not user_library_entry:
            return {'message': 'Book not found in your library'}, 404

        db.session.delete(user_library_entry)
        db.session.commit()

        return {'message': 'Book successfully removed from your library'}, 200
