
# Look at item.py for a detailed description of what is going on
# These are pretty much the same, minor diffrences

from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type = str,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('password',
        type = str,
        required=True,
        help="This field cannot be left blank!"
    )
    def post(self):
        data = UserRegister.parser.parse_args()
        if UserModel.find_by_userid(data['username']):
            return {'message': "A user with a that Username already exists."}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message":"User created sucessfuly"}, 201
