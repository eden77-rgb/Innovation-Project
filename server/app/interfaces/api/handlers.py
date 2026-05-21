from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from domain.exceptions import ValidationError, InfrastructureError


def register_exception_handler(app: FastAPI):

    @app.exception_handler(ValidationError)
    def validation_handler(request: Request, exc: ValidationError):
        return JSONResponse(
            status_code=400,
            content={
                "error": "VALIDATION_ERROR",
                "message": str(exc)
            }
        )


    @app.exception_handler(InfrastructureError)
    def infrastructure_handler(request: Request, exc: InfrastructureError):
        return JSONResponse(
            status_code=503,
            content={
                "error": "INFRASTRUCTURE_ERROR",
                "message": str(exc)
            }
        )
