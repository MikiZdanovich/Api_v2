from typing import Union, Dict, List
from celery_app import app as celery
import requests


@celery.task
def get_data_from_git_api(nickname: str) -> Union[Dict[str, str], List[str]]:
    url = "https://api.github.com/users/{}/repos".format(nickname)
    response = requests.get(url)
    result = {"status": response.status_code, "data": response.json()}
    return result


def parse_response(result) -> Union[str, Dict[int, str]]:
    if result["status"] == 200:
        if result["data"]:
            list_repos = [item["name"] for item in result["data"]]
            return str(list_repos)
    else:
        return "This is invalid git nick_name"


def get_repos(nickname: str) -> Union[str, dict]:
    async_response = get_data_from_git_api.delay(nickname=nickname)
    response = async_response.get()
    result: Union[str, dict] = parse_response(response)
    return result
