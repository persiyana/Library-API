"""
Library Management API.

This module initializes a Flask application with RESTful API endpoints for:
- User registration and authentication.
- User profile management.
- Book retrieval and review functionality.
- User library management.
- Admin promotion.

The API uses SQLite as the database and JWT for authentication.

Routes:
    - /api/register/ : Register a new user.
    - /api/login/ : User login with JWT token generation.
    - /api/profile/ : Retrieve user profile information.
    - /api/books/ : Fetch all books or a specific book by ID.
    - /api/books/<book_id>/review/ : Submit a book review.
    - /api/library/ : Manage user's book reading statuses.
    - /api/promote-to-admin/ : Promote a user to admin role.

Dependencies:
    - Flask
    - Flask-RESTful
    - Flask-JWT-Extended
    - SQLAlchemy
"""
import os
import requests

from flask import Flask, request, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager


from models import db
from resources.register import Register
from resources.login import Login
from resources.user_profile import UserProfile
from resources.books import Books
from resources.book_review import BookReview
from resources.user_library import UserLibrary
from resources.promote_to_admin import PromoteToAdmin

app = Flask(__name__, template_folder='./templates/')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY", "secret_key")

db.init_app(app)
api = Api(app)
jwt = JWTManager(app)

api.add_resource(Register, '/api/register/')
api.add_resource(Login, '/api/login/')
api.add_resource(UserProfile, '/api/profile/')
api.add_resource(Books, '/api/books/', '/api/books/<int:book_id>/')
api.add_resource(BookReview, '/api/books/<int:book_id>/review/')
api.add_resource(UserLibrary, '/api/library/')
api.add_resource(PromoteToAdmin, '/api/promote-to-admin/')

@app.route('/books', methods=['GET'])
def get_books():
    """
    Retrieve books based on optional query parameters (title, author, genre).

    This route proxies the request to the backend API and returns the book list.

    Query Parameters:
        title (str, optional): Filter books by title.
        author (str, optional): Filter books by author.
        genre (str, optional): Filter books by genre.

    Returns:
        JSON response with book data or an error message if no books are found.
    """
    title = request.args.get('title')
    author = request.args.get('author')
    genre = request.args.get('genre')

    params = {}
    if title:
        params['title'] = title
    if author:
        params['author'] = author
    if genre:
        params['genre'] = genre

    response = requests.get('http://localhost:5000/api/books/', params=params, timeout = 5)

    if response.status_code == 404:
        return jsonify({'message': 'No books found'}), 404

    return jsonify(response.json()), response.status_code

if __name__ == '__main__':
    app.debug = True
    app.run()
