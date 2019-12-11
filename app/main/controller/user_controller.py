from flask import request
from flask_restplus import Resource

from ..util.dto import UserDto
from ..service.user_service import save_new_user, get_all_users, get_repos

api = UserDto.api
_user = UserDto.user


@api.route('/')
class UserList(Resource):
    @api.doc('list_of_saved_users')
    @api.marshal_list_with(_user, envelope='data')
    def get(self):
        """List all saved  users"""
        return get_all_users()

    @api.response(201, 'User successfully created.')
    @api.doc('create a new user')
    @api.expect(_user, validate=True)
    def post(self):
        """Creates a new User """
        data = request.json
        return save_new_user(data=data)


@api.route('/<username>')
@api.param('username', 'The User Git name')
@api.response(404, 'User not found.')
class User(Resource):
    @api.doc('get a user')
    @api.marshal_with(_user)
    def get(self, username):
        """get a user given its identifier"""
        user = get_repos(username)
        if not user:
            api.abort(404)
        else:
            return user

