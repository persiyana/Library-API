from flask import Flask
from flask_sqlalchemy import SQLAlchemy
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

app = Flask(__name__)
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

if __name__ == '__main__':
    app.run(debug=True)
