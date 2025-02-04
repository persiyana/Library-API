from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash
from models import db
from models.user_model import UserModel

class Register(Resource):
    def post(self):
        args = reqparse.RequestParser()
        args.add_argument('name', type=str, required=True)
        args.add_argument('email', type=str, required=True)
        args.add_argument('password', type=str, required=True)
        data = args.parse_args()

        if UserModel.query.filter_by(email=data['email']).first():
            return {'message': 'Email already registered'}, 400

        user = UserModel(name=data['name'], email=data['email'], password=generate_password_hash(data['password']))
        db.session.add(user)
        db.session.commit()
        return {'message': 'User registered successfully'}, 201