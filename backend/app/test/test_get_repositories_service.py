import pytest
from werkzeug.exceptions import Forbidden, InternalServerError, NotFound
from app.main.service.get_repositories_service import parse_response


class TestParseResponse:
    """parse_response parse response from Git Api,
    and return List of repositories, or rise exception"""

    @pytest.mark.parametrize('response,result', [
        ({"status": 200, "data": [{'name': "repo_one"}, {'name': "repo_two"}]}, ["repo_one", "repo_two"]),
        ({"status": 200, "data": []}, [])
    ]
                             )
    def test_pr_ok(self, response, result):
        assert parse_response(response) == result
        assert isinstance(parse_response(response), list)

    @pytest.mark.parametrize("exception,response", [
        (Forbidden, {"status": 403, "data": [{"name": "repo_one"}]}),
        (InternalServerError, {"status": 500, "data": [{"name": "repo_one"}]}),
        (NotFound, {"status": 404, "data": [{"name": "repo_one"}]}),
        (InternalServerError, {"status": 505, "data": []})
    ]
                             )
    def test_pr_not_ok(self, exception, response):
        with pytest.raises(exception):
            parse_response(response)

class TestGetDataFromGit:
    """test_data_from_git_api accept Git username, make get request
    to Git api, and retun Dict with status_code and List of user repositories"""