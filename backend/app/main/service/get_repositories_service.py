from typing import Union, Dict, List

import requests
from requests.models import Response

from backend.app.main.util.exceptions import GitUserNotFound, GitHubServerUnavailable


def get_data_from_git_api(nickname: str) -> Dict[str, Union[int, List]]:
    url: str = "https://api.github.com/users/{}/repos".format(nickname)
    response: Response = requests.get(url)
    result: Dict[str, Union[int, List]] = {"status": response.status_code, "data": response.json()}
    return result


def parse_response(result: Dict[str, Union[int, List]]) -> [List, str]:
    if result["status"] == 200:
        list_repos: List = [item["name"] for item in result["data"]]
        return list_repos
    elif result['status'] == 404:
        raise GitUserNotFound
    else:
        raise GitHubServerUnavailable


def get_repos(nickname: str) -> [List, str]:
    response = get_data_from_git_api(nickname)
    result: List = parse_response(response)
    return result


if __name__ == "__main__":
    result = get_repos("string")
    print(type(result))
    print(result)
