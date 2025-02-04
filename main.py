from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
import requests
from flask_restful import Api
from flask_jwt_extended import JWTManager
import os

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

    response = requests.get('http://localhost:5000/api/books/', params=params)

    if response.status_code == 404:
        return jsonify({'message': 'No books found'}), 404

    return jsonify(response.json()), response.status_code

if __name__ == '__main__':
    app.debug = True
    app.run()
