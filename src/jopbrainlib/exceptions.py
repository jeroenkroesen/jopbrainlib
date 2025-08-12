"""Custom exceptions for JopBrainLib
"""


class AuthorizationDeniedError(Exception):
    """The Joplin user has explicitly denied a request for an API token
    """
    pass
