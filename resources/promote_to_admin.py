from flask_restful import reqparse, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user_model import UserModel
from models import db

class PromoteToAdmin(Resource):
    @jwt_required()
    def post(self):
        current_user_id = get_jwt_identity()
        current_user = UserModel.query.get(current_user_id)

        assert isinstance(current_user, UserModel), "User must be an instance of UserModel"
        
        if current_user.role != 'admin':
            return {'message': 'You must be an admin to perform this action'}, 403

        args = reqparse.RequestParser()
        args.add_argument('username', type=str, required=True, help='Username of the user to promote')
        data = args.parse_args()

        user_to_promote = UserModel.query.filter_by(name=data['username']).first()

        if not user_to_promote:
            return {'message': 'User not found'}, 404

        if user_to_promote.role == 'admin':
            return {'message': 'This user is already an admin'}, 400

        user_to_promote.role = 'admin'
        db.session.commit()

        return {'message': f'User {data["username"]} has been promoted to admin'}, 200