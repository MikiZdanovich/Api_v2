import datetime

from app.main import db
from app.main.model.users import User
from app.main.service.get_repositories_service import get_repos


def new_user(data, repositories):
    user = User(username=data['username'],
                repositories=repositories,
                requested_on=datetime.datetime.utcnow())
    save_changes(user)
    return user


def updated_user(data, repositories):
    user = User.query.filter_by(username=data['username']).first()
    user.repositories = repositories
    save_changes(user)
    return user


def existing_user(data):
    user = User.query.filter_by(username=data["username"]).first()
    return user



def get_user_repositories(data):

    try:
        repositories = get_repos(data['username'])
        git_user = existing_user(data)
        if git_user:
            if repositories != git_user.repositories:
                user = updated_user(data, repositories)
            else:
                user = existing_user(data)
        else:
            user = new_user(data, repositories)

    except NameError:
        response_object = {
            'user name': data["username"],
            'repositories': "Invalid nick name"
        }

    else:
        response_object = {
            'user name': user.username,
            'repositories': user.repositories
        }

    finally:
        return response_object

def get_all_saved_users():
    return User.query.all()


def save_changes(data):
    db.session.add(data)
    db.session.commit()
