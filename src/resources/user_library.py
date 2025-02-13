"""
This module defines the `UserLibrary` resource for managing a user's library.
It allows users to add, update, retrieve, and delete books in their personal library.
"""
from flask_restful import reqparse, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user_library_model import UserLibraryModel
from src.models import db

class UserLibrary(Resource):
    """
    Represents the resource for managing the user's book library. 
    It provides the ability to retrieve, add, update, and delete books in the library, 
    based on their status.
    """
    @jwt_required()
    def get(self):
        """
        Handles the GET request to retrieve all books from the user's library.
        It categorizes the books into three statuses: 'read', 'currently reading', 
        and 'want to read'.
        """
        current_user_id = get_jwt_identity()

        read_books = UserLibraryModel.query.filter_by(user_id=current_user_id,
                                                      status="completed").all()
        reading_books = UserLibraryModel.query.filter_by(user_id=current_user_id,
                                                         status="reading").all()
        want_to_read_books = UserLibraryModel.query.filter_by(user_id=current_user_id,
                                                              status="wishlist").all()

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
        """
        current_user_id = get_jwt_identity()
        args = reqparse.RequestParser()
        args.add_argument('book_id', type=int, required=True, help='Book ID is required')
        args.add_argument('status', type=str, required=True,
                          help='Status (completed, wishlist, reading)')
        data = args.parse_args()

        if data['status'] not in ["completed", "wishlist", "reading"]:
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
    def patch(self, book_id):
        """
        Handles the PATCH request to update the status of a book in the user's library.
        
        The method checks if the book exists in the library and if the new status is valid.
        If valid, it updates the book's status.
        """
        current_user_id = get_jwt_identity()
        args = reqparse.RequestParser()
        args.add_argument('new_status', type=str, required=True,
                          help='New status (completed, wishlist, reading)')
        data = args.parse_args()

        if data['new_status'] not in ["completed", "wishlist", "reading"]:
            return {'message': 'Invalid status'}, 400

        user_library_entry = UserLibraryModel.query.filter_by(user_id=current_user_id,
                                                              book_id=book_id).first()
        if not user_library_entry:
            return {'message': 'Book not found in your library'}, 404

        user_library_entry.status = data['new_status']
        db.session.commit()

        return {'message': f'Book status updated to {data["new_status"]}'}, 200

    @jwt_required()
    def delete(self, book_id):
        """
        Handles the DELETE request to remove a book from the user's library.
        
        The method checks if the book exists in the library. If it does, the book is deleted.
        """
        current_user_id = get_jwt_identity()

        user_library_entry = UserLibraryModel.query.filter_by(user_id=current_user_id,
                                                              book_id=book_id).first()

        if not user_library_entry:
            return {'message': 'Book not found in your library'}, 404

        db.session.delete(user_library_entry)
        db.session.commit()

        return {'message': 'Book successfully removed from your library'}, 200
