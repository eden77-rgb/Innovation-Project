from .base import AppError

class InfrastructureError(AppError):
    """Base class for infrastructure errors"""
    pass


class PromptTemplateNotFoundError(InfrastructureError):
    pass


class OllamaNotAvailableError(InfrastructureError):
    pass


class OllamaTimeoutError(InfrastructureError):
    pass


class OllamaGenerationError(InfrastructureError):
    pass
