"""
Library Management API.
"""
import os
import requests

from flask import Flask, request, jsonify, Response
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

def create_app(config="default"):
    """Application factory to create app instances dynamically."""
    app = Flask(__name__, template_folder='./templates/')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY", "secret_key")

    if config == "testing":
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"
        app.config['TESTING'] = True

    db.init_app(app)
    api = Api(app)
    jwt = JWTManager(app)
    _ = jwt

    api.add_resource(Register, '/api/register/')
    api.add_resource(Login, '/api/login/')
    api.add_resource(UserProfile, '/api/profile/')
    api.add_resource(Books, '/api/books/', '/api/books/<int:book_id>/')
    api.add_resource(BookReview, '/api/books/<int:book_id>/review/')
    api.add_resource(UserLibrary, '/api/library/', '/api/library/<int:book_id>/')
    api.add_resource(PromoteToAdmin, '/api/promote-to-admin/')

    @app.route('/books', methods=['GET'])
    def get_books() -> tuple[Response, int]:
        """
        Retrieve books based on optional query parameters (title, author, genre).

        This route proxies the request to the backend API and returns the book list.
        """
        title: str | None = request.args.get('title')
        author: str | None  = request.args.get('author')
        genre: str | None  = request.args.get('genre')

        params: dict[str, str] = {}
        if title:
            params['title'] = title
        if author:
            params['author'] = author
        if genre:
            params['genre'] = genre

        try:
            response: requests.Response = requests.get('http://localhost:5000/api/books/',
                                                       params=params, timeout=5)
        except requests.RequestException:
            return jsonify({'message': 'Error retrieving books'}), 500

        return jsonify(response.json()), response.status_code


    return app

if __name__ == '__main__':
    app2 = create_app()
    app2.debug = True
    app2.run()
