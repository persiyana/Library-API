from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from models.user_model import UserModel

class Login(Resource):
    def post(self):
        args = reqparse.RequestParser()
        args.add_argument('email', type=str, required=True)
        args.add_argument('password', type=str, required=True)
        data = args.parse_args()

        user = UserModel.query.filter_by(email=data['email']).first()
        if not user:
            return {'message': 'Invalid user'}, 401
        
        if not check_password_hash(user.password, data['password']): 
            return {'message': 'Invalid pass'}, 401

        access_token = create_access_token(identity=user.id)
        return {'access_token': access_token}, 200