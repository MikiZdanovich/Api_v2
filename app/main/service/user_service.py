import uuid
import datetime
from app.main.service.get_repositories_service import get_repos
from app.main import db
from app.main.model.users import User


def save_new_user(data):
    user = User.query.filter_by(username=data['username']).first()
    if not user:
        new_user = User(

            username=data['username'],
            repositories=get_repos(data['username']),
            requested_on=datetime.datetime.utcnow()
        )
        save_changes(new_user)
        response_object = {
            'status': 'success',
            'repositories': new_user.repositories,
            'message': 'Successfully saved.'
        }
        return response_object, 201
    else:
        updated_repos = get_repos(nickname=data["username"])
        if User.query.filter_by(username=data["username"]).first().repositories == updated_repos:
            response_object = {
                'status': 'fail',
                'message': 'User already exists.',
                'repositories': User.query.filter_by(username=data["username"]).first().repositories
            }
            return response_object, 409
        else:
            User.query.filter_by(username=data["username"]).first().repositories = updated_repos
            response_object = {
                'status': 'updated',
                'message': 'User repositories successfully updated',
                'repositories': User.query.filter_by(username=data["username"]).first().repositories
            }
            return response_object


def get_all_users():
    return User.query.all()


def save_changes(data):
    db.session.add(data)
    db.session.commit()
