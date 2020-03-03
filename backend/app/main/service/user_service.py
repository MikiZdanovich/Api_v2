from typing import Dict, List, Union

from sqlalchemy.engine import RowProxy, ResultProxy

from backend.app.main.model.users import user
from backend.app.main.service.get_repositories_service import get_repos
from backend.app.main.util.exceptions import GitHubServerUnavailable
from backend.database import Session
from backend.make_celery import celery


def new_user(data: Dict[str, str], repositories: List) -> Dict[str, str]:
    session = Session()
    session.execute(user.insert().values(username=data['username'], repositories=repositories))
    session.commit()
    response = {'username': data['username'], "repositories": repositories}
    return response


def update_user(data: Dict[str, str], repositories: List) -> Dict[str, str]:
    session = Session()
    session.execute(user.update().where(user.c.username == data['username']).values(repositories=repositories))
    session.commit()
    response = {"username": data['username'], "repositories": repositories}
    return response


def existing_user(data: Dict[str, str]) -> RowProxy:
    session = Session()
    result = session.execute(user.select(user.c.username == data['username']))
    return result.fetchone()


@celery.task(autoretry_for=(GitHubServerUnavailable,), retry_kwargs={'max_retries': 5, 'countdown': 5})
def get_user_repositories(data: Dict[str, str]) -> Dict[str, Union[str, List]]:
    repositories: List = get_repos(data['username'])
    git_user: RowProxy = existing_user(data)
    if existing_user(data):
        if ",".join(repositories) != git_user['repositories'].strip("{}"):
            git_user: Dict[str, str] = update_user(data, repositories)
    else:
        git_user: Dict[str, str] = new_user(data, repositories)

    response_object: Dict[str, str] = {
        'user name': git_user['username'],
        'repositories': git_user['repositories']
    }
    return response_object


def get_all_saved_users() -> List[Dict[str, str]]:
    session = Session()
    result: ResultProxy = session.execute(user.select()).fetchall()
    response = [{'username:': row['username'], 'repositories': row['repositories']} for row in result]
    return response
