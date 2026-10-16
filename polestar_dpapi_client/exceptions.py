"""Exceptions for the Polestar API module."""


class PolestarAPIError(Exception):
    """Base exception for Polestar API errors."""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code


class AuthenticationError(PolestarAPIError):
    """Raised when authentication fails (invalid credentials, token expired, etc.)."""
    pass


class ApiRequestError(PolestarAPIError):
    """Raised when an API request fails."""
    pass
