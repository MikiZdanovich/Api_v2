import datetime
from time import sleep

from app.main import db
from app.main.model.users import User
from app.main.service.get_repositories_service import get_repos
from celery_app import app as celery


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


@celery.task(bind=True)
def get_user_repositories(data):
    try:
        repositories = get_repos(data['username'])
        if existing_user(data):
            git_user = existing_user(data)
            if repositories != git_user.repositories:
                user = updated_user(data, repositories)
            else:
                user = existing_user(data)
        else:
            user = new_user(data, repositories)

        response_object = {
            'user name': user.username,
            'repositories': user.repositories
        }
        sleep(100)
        return response_object
    except Exception:
        return {"Exception": "User not Found"}
    # except CustomException:
    # отложеное выполнение таски


def get_all_saved_users():
    return User.query.all()


def save_changes(data):
    db.session.add(data)
    db.session.commit()
