from typing import Union, Dict, List
import requests


def get_data_from_git_api(nickname: str) -> Union[Dict[str, str], List[str]]:
    url = "https://api.github.com/users/{}/repos".format(nickname)
    response = requests.get(url)

    return response


def parse_response(response) -> Union[str, Dict[int, str]]:
    if response.status_code == 200:
        list_repos = [item["name"] for item in response.json()]
        return str(list_repos)

    else:
        return "This is invalid git nick_name"


def get_repos(nickname: str) -> Union[str, dict]:
    response = get_data_from_git_api(nickname)
    result: Union[str, dict] = parse_response(response)
    return result
