class AppError(Exception):
    """Base class for exception in services/ (not binding with FastAPI)."""


class NotFoundError(AppError):
    pass


class ConflictError(AppError):
    pass


class UnauthorizedError(AppError):
    pass


class ForbiddenError(AppError):
    pass