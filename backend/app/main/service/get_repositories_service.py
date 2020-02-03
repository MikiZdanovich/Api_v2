from typing import Union, Dict, List
from celery_app import app as celery
import requests


def get_data_from_git_api(nickname: str) -> Union[Dict[str, str], List[str]]:
    url = "https://api.github.com/users/{}/repos".format(nickname)
    response = requests.get(url)
    result = {"status": response.status_code, "data": response.json()}
    return result


def parse_response(result) -> List:
    if result["status"] == 200:
        list_repos = [item["name"] for item in result["data"]]
        return list_repos
    else:
        raise NameError("Invalid git Nickname")


def get_repos(nickname: str) -> List:
    response = get_data_from_git_api(nickname)
    result = parse_response(response)
    return result


