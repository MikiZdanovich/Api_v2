from flask import request, url_for
from flask_restplus import Resource

from app.main.service.user_service import get_user_repositories, get_all_saved_users
from app.main.util.dto import UserDto

api = UserDto.api
_user = UserDto.user
# task_api = TaskDto.api


@api.route('/')
class UserList(Resource):
    @api.doc('list_of_saved_users')
    @api.marshal_list_with(_user, envelope='data')
    def get(self):
        """List all saved  users"""
        return get_all_saved_users()

    @api.response(202, 'Git repositories of current user.')
    @api.doc('Get User git Repos')
    @api.expect(_user, validate=True)
    def post(self):
        """Get User git Repos"""
        data = request.json
        task = get_user_repositories.apply_async(data=data)
        return {}, {'Location': url_for('.user_task',
                                        task_id=task.id)}


@api.route("/<task_id>")
class Task(Resource):
    def task_status(self, task_id):
        """Async Task"""
        task = get_user_repositories.AsyncResult(task_id)
        if task.state == 'PENDING':
            response = {
                'state': task.state,
                'status': 'Pending...'
            }
        elif task.state != 'FAILURE':
            response = {
                'state': task.state,
                'status': task.info.get('status', '')
            }
            if 'result' in task.info:
                response['result'] = task.info['result']
        else:

            response = {
                'state': task.state,
                'status': str(task.info),
            }
        return response
