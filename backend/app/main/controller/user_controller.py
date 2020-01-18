from flask import request
from flask_restplus import Resource

from app.main.service.user_service import get_user_repositories, get_all_saved_users
from app.main.util.dto import UserDto

api = UserDto.api
_user = UserDto.user


@api.route('/')
class UserList(Resource):
    @api.doc('list_of_saved_users')
    @api.marshal_list_with(_user, envelope='data')
    def get(self):
        """List all saved  users"""
        return get_all_saved_users()

    @api.response(200, 'Git repositories of current user.')
    @api.doc('Get User git Repos')
    @api.expect(_user, validate=True)
    def post(self):
        """Get User git Repos"""
        data = request.json
        return get_user_repositories(data=data)


