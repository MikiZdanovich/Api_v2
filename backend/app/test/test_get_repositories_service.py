import pytest
import requests
from requests import Response
from werkzeug.exceptions import Forbidden, InternalServerError, NotFound
from app.main.service.get_repositories_service import parse_response, get_data_from_git_api


# Just for fun fixture
@pytest.fixture(autouse=True, params=[1])
def setup():
    print(f"HeyHo, Fixture set up {1}")
    yield
    print(f"Buy, Fixture tear-down")


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


class MockResponseOk:
    def __init__(self):
        self.status_code = 200

    @staticmethod
    def json():
        return [{"Test": "test"}, {"name": ["repo1"]}]

    @pytest.fixture
    def mock_response(self, monkeypatch):
        """Requests.get() mocked to return {"status": 200, "data": [{"Test": "test"}, {"name": ["repo1"]}]."""

        def mock_get(*args, **kwargs):
            return MockResponseOk()

        monkeypatch.setattr(requests, "get", mock_get)


class TestGetDataFromGit:
    """test_data_from_git_api accept Git username, make get request
    to Git api, and return Dict with status_code and List of user repositories"""

    @staticmethod
    def json():
        return [{"Test": "test"}, {"name": ["repo1"]}]

    @pytest.fixture
    def mock_response(self, monkeypatch):
        """Requests.get() mocked to return {"status": 200, "data": [{"Test": "test"}, {"name": ["repo1"]}]."""

        def mock_get(*args, **kwargs):
            return MockResponseOk()

        monkeypatch.setattr(requests, "get", mock_get)

    def test_get_data_from_git_api(self, mock_response):
        setup = {"status": 200, "data": [{"Test": "test"}, {"name": ["repo1"]}]}
        assert get_data_from_git_api("test") == setup
