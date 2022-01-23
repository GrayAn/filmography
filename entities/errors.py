class ApplicationError(Exception):
    """Generic application error"""


class ObjectDoesNotExistError(ApplicationError):
    """Object does not exist"""
