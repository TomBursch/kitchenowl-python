"""KitchenOwl exceptions."""


class KitchenOwlException(Exception):
    """Raised when a general exception occours."""


class KitchenOwlRequestException(KitchenOwlException):
    """Raised on a bad request to the KitchenOwl instance."""


class KitchenOwlAuthException(KitchenOwlException):
    """Raised when the authentication token is not valid."""
