from .base import AppError

class ValidationError(AppError):
    """Base class for validation errors"""
    pass


class EmptyPromptError(ValidationError):
    pass


class InvalidPromptTypeError(ValidationError):
    pass
