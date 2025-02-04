from flask_restful import reqparse, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user_library_model import UserLibraryModel
from extensions import db

class UserLibrary(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()

        read_books = UserLibraryModel.query.filter_by(user_id=current_user_id, status="Прочетени").all()
        reading_books = UserLibraryModel.query.filter_by(user_id=current_user_id, status="Чета в момента").all()
        want_to_read_books = UserLibraryModel.query.filter_by(user_id=current_user_id, status="Искам да прочета").all()

        return {
            'read_books': [{'book_id': entry.book_id, 'title': entry.book.title} for entry in read_books],
            'reading_books': [{'book_id': entry.book_id, 'title': entry.book.title} for entry in reading_books],
            'want_to_read_books': [{'book_id': entry.book_id, 'title': entry.book.title} for entry in want_to_read_books]
        }, 200

    @jwt_required()
    def post(self):
        current_user_id = get_jwt_identity()
        args = reqparse.RequestParser()
        args.add_argument('book_id', type=int, required=True, help='Book ID is required')
        args.add_argument('status', type=str, required=True, help='Status (Прочетени, Чета в момента, Искам да прочета)')
        data = args.parse_args()

        if data['status'] not in ["Прочетени", "Чета в момента", "Искам да прочета"]:
            return {'message': 'Invalid status'}, 400

        existing_entry = UserLibraryModel.query.filter_by(user_id=current_user_id, book_id=data['book_id']).first()
        if existing_entry:
            return {'message': 'Book already in your library'}, 400

        user_library_entry = UserLibraryModel(
            user_id=current_user_id,
            book_id=data['book_id'],
            status=data['status']
        )
        db.session.add(user_library_entry)
        db.session.commit()

        return {'message': 'Book added to library with status {}'.format(data['status'])}, 201

    @jwt_required()
    def patch(self):
        current_user_id = get_jwt_identity()
        args = reqparse.RequestParser()
        args.add_argument('book_id', type=int, required=True, help='Book ID is required')
        args.add_argument('new_status', type=str, required=True, help='New status (Прочетени, Чета в момента, Искам да прочета)')
        data = args.parse_args()

        if data['new_status'] not in ["Прочетени", "Чета в момента", "Искам да прочета"]:
            return {'message': 'Invalid status'}, 400

        user_library_entry = UserLibraryModel.query.filter_by(user_id=current_user_id, book_id=data['book_id']).first()
        if not user_library_entry:
            return {'message': 'Book not found in your library'}, 404

        user_library_entry.status = data['new_status']
        db.session.commit()

        return {'message': 'Book status updated to {}'.format(data['new_status'])}, 200

    @jwt_required()
    def delete(self):
        current_user_id = get_jwt_identity()
        args = reqparse.RequestParser()
        args.add_argument('book_id', type=int, required=True, help='Book ID is required')
        data = args.parse_args()

        user_library_entry = UserLibraryModel.query.filter_by(user_id=current_user_id, book_id=data['book_id']).first()

        if not user_library_entry:
            return {'message': 'Book not found in your library'}, 404

        db.session.delete(user_library_entry)
        db.session.commit()

        return {'message': 'Book successfully removed from your library'}, 200