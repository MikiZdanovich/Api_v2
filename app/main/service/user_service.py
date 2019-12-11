import uuid
import datetime
from app.main.service.repositories_get_service import get_repos
from app.main import db
from app.main.model.repos import User


def save_new_user(data):
    user = User.query.filter_by(username=data['username']).first()
    if not user:
        new_user = User(
            public_id=str(uuid.uuid4()),
            username=data['username'],
            list_repositories=get_repos(data['username']),
            registered_on=datetime.datetime.utcnow()
        )
        save_changes(new_user)
        response_object = {
            'status': 'success',
            'message': 'Successfully added.'
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'User already exists.',
        }
        return response_object, 409


def get_all_users():
    return User.query.all()


#
# def get_a_user(public_id):
#     return User.query.filter_by(public_id=public_id).first()

def get_a_user_repos_list(username):
    user = User.query.filter_by(username=username).first()
    return user.list_repositories


def save_changes(data):
    db.session.add(data)
    db.session.commit()
