from werkzeug.exceptions import HTTPException


class GitUserNotFound(HTTPException):
    """*404* CUSTOM `Not Found`

     Raise if a git user  does not exist.
     """

    code = 404
    description = (
        "Failed to found corresponding Git user. "
        "Please check Git user name and try again"
    )


class GitHubServerUnavailable(HTTPException):
    """*5xx* Connection issue`

     Raise in case any exception with GitHub except 404 occur
     """

    code = 500
    description = (
        "Failed to get repositories "
        "Connection failed after max retries."

    )
