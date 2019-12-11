from flask_restplus import Namespace, fields


class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {

        'username': fields.String(required=True, description='user username'),
        'repositories': fields.String(required=False, description='user repositories'),
        'public_id': fields.String(required=False, description='user Identifier')
    })
