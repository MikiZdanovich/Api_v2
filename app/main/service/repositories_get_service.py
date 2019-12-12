from typing import Union, Dict, List, Tuple
import requests

def get_data_from_git_api(nickname: str) -> Union[Dict[str, str], List[str]]:
    url = "https://api.github.com/users/{}/repos".format(nickname)
    response = requests.get(url)

    return response.json()


def parse_response(response) -> Union[str, Dict[int, str]]:

    if isinstance(response, dict):
        return "This is invalid git nick_name"
    else:
        list_repos = [item["name"] for item in response]
        return str(list_repos)


def get_repos(nickname: str) -> Tuple[str, Union[str, dict]]:
    response = get_data_from_git_api(nickname)
    result: Union[str, dict] = parse_response(response)
    return result

