"""Application errors."""

from typing import Any


class AppError(Exception):
    """Base application error."""

    def __init__(
        self,
        message: str,
        status_code: int = 500,
        details: dict[str, Any] | None = None,
    ) -> None:
        """Initialize error."""
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class ValidationError(AppError):
    """Validation error."""

    def __init__(self, message: str, details: dict[str, Any] | None = None) -> None:
        """Initialize validation error."""
        super().__init__(message, status_code=400, details=details)


class NotFoundError(AppError):
    """Resource not found error."""

    def __init__(self, resource: str, identifier: str) -> None:
        """Initialize not found error."""
        message = f"{resource} with identifier '{identifier}' not found"
        super().__init__(message, status_code=404)


class UnauthorizedError(AppError):
    """Unauthorized error."""

    def __init__(self, message: str = "Unauthorized") -> None:
        """Initialize unauthorized error."""
        super().__init__(message, status_code=401)


class ForbiddenError(AppError):
    """Forbidden error."""

    def __init__(self, message: str = "Forbidden") -> None:
        """Initialize forbidden error."""
        super().__init__(message, status_code=403)
