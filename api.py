from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity 
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__) 

app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
if not app.config['JWT_SECRET_KEY']:
    raise ValueError("JWT_SECRET_KEY is missing in .env file!")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app) 
api = Api(app)
jwt = JWTManager(app)

class UserModel(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(10), default="user")

    def __init__(self, name, email, password, role = "user"):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)
        self.role = role
    
    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self): 
        return f"User(name = {self.name}, email = {self.email})"

user_args = reqparse.RequestParser()
user_args.add_argument('name', type=str, required=True, help="Name cannot be blank")
user_args.add_argument('email', type=str, required=True, help="Email cannot be blank")
user_args.add_argument('password', type=str, required=True, help="Password cannot be blank")

login_args = reqparse.RequestParser()
login_args.add_argument('email', type=str, required=True, help="Email cannot be blank")
login_args.add_argument('password', type=str, required=True, help="Password cannot be blank")

userFields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String,
    'role': fields.String
}

class Register(Resource):
    def post(self):
        args = user_args.parse_args()
        if UserModel.query.filter_by(email=args["email"]).first():
            return {'message': 'Email already exists'}, 400

        user = UserModel(name=args["name"], email=args["email"], password=args["password"])
        db.session.add(user)
        db.session.commit()
        return {'message': 'User created successfully'}, 201

class Login(Resource):
    def post(self):
        args = login_args.parse_args()
        user = UserModel.query.filter_by(email=args["email"]).first()
        if user and user.verify_password(args["password"]):
            access_token = create_access_token(identity=user.id)
            return {'access_token': access_token}, 200
        return {'message': 'Invalid credentials'}, 401

class Users(Resource):
    @jwt_required()
    @marshal_with(userFields)
    def get(self):
        print("Current User ID: ", get_jwt_identity())
        users = UserModel.query.all() 
        return users 
    


class User(Resource):
    @jwt_required()
    @marshal_with(userFields)
    def get(self, id):
        user = UserModel.query.filter_by(id=id).first() 
        if not user: 
            abort(404, message="User not found")
        return user 
    
class Profile(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = UserModel.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 404
        return {"id": user.id, "name": user.name, "email": user.email, "role": user.role}, 200  
    
    
api.add_resource(Register, '/api/register/')
api.add_resource(Login, '/api/login/')
api.add_resource(Users, '/api/users/')
api.add_resource(User, '/api/users/<int:id>')
api.add_resource(Profile, "/api/profile/")

@app.route('/')
def home():
    return '<h1>Flask</h1>'

if __name__ == '__main__':
    app.run(debug=True)