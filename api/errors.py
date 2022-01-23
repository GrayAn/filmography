class BaseAPIError(Exception):
    """
    Base exception class for raising HTTP errors.
    """
    status: int = None
    message: str = None

    def __init__(self, message: str = None):
        super().__init__()
        self.message = message or self.message


class BadRequestError(BaseAPIError):
    status = 400
    message = "The request is incorrect"

    def __init__(self, message: str = None, errors: dict = None):
        super().__init__(message=message)
        self.errors = errors


class NotFoundError(BaseAPIError):
    status = 404
    message = "The requested resource not found"


class MethodNotAllowedError(BaseAPIError):
    status = 405
    message = "This method is not allowed to use with this URL"
