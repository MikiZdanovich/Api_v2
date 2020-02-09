import datetime
from typing import Union, Dict, List
from app.main.model.users import User
from app.main.service.get_repositories_service import get_repos
from database import db
from make_celery import celery


def new_user(data: Dict[str, str], repositories: List) -> User:
    user: User = User(username=data['username'],
                repositories=repositories,
                requested_on=datetime.datetime.utcnow())
    save_changes(user)
    return user


def updated_user(data: Dict[str, str], repositories: List) -> User:
    user: User = User.query.filter_by(username=data['username']).first()
    user.repositories = repositories
    save_changes(user)
    return user


def existing_user(data):
    user = User.query.filter_by(username=data["username"]).first()
    return user


@celery.task()
def get_user_repositories(data):
    repositories = get_repos(data['username'])
    if existing_user(data):
        if repositories != existing_user(data).repositories:
            user = updated_user(data, repositories)
        else:
            user = existing_user(data)
    else:
        user = new_user(data, repositories)
    response_object = {
        'user name': user.username,
        'repositories': user.repositories
    }
    return response_object


# except Exception:
#     return {"Exception": "User not Found"}
# except CustomException:
# отложеное выполнение таски


def get_all_saved_users():
    return User.query.all()


def save_changes(data):
    db.session.add(data)
    db.session.commit()
