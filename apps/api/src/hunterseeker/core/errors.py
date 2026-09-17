"""Standard error envelope.

Every non-2xx response from the API has the shape::

    {"error": {"code": "<machine-readable>", "message": "<human-readable>", "details": ...}}

``code`` is a stable snake_case identifier clients can branch on; ``message`` is for
humans and may change; ``details`` is free-form JSON (validation errors, field names,
etc.) or ``null``. Raise :class:`ApiError` from domain code to produce one deliberately;
the handlers below also normalise FastAPI/Starlette's own exceptions into the same shape.
"""

from http import HTTPStatus
from typing import Any

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from starlette.exceptions import HTTPException as StarletteHTTPException

type JsonValue = dict[str, Any] | list[Any] | str | int | float | bool | None


class ErrorBody(BaseModel):
    """The ``error`` object inside the envelope."""

    code: str = Field(description="Stable, machine-readable identifier, e.g. `not_found`.")
    message: str = Field(description="Human-readable explanation. Not stable; do not parse.")
    details: JsonValue = Field(default=None, description="Free-form context, or null.")


class ErrorEnvelope(BaseModel):
    """Body of every error response."""

    error: ErrorBody


class ApiError(Exception):
    """Raise from domain code to return a structured error to the client."""

    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
        details: JsonValue = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.code = code
        self.message = message
        self.details = details


class NotFoundError(ApiError):
    """404 with ``code="not_found"``."""

    def __init__(self, message: str = "Not found.", details: JsonValue = None) -> None:
        super().__init__(404, "not_found", message, details)


def error_response(
    status_code: int, code: str, message: str, details: JsonValue = None
) -> JSONResponse:
    """Build a JSON response carrying the envelope."""
    body = ErrorEnvelope(error=ErrorBody(code=code, message=message, details=details))
    return JSONResponse(status_code=status_code, content=body.model_dump(mode="json"))


def code_for_status(status_code: int) -> str:
    """Default ``code`` for a bare HTTP status, e.g. 404 -> ``not_found``."""
    try:
        return HTTPStatus(status_code).phrase.lower().replace(" ", "_").replace("-", "_")
    except ValueError:
        return f"http_{status_code}"


async def _handle_api_error(_request: Request, exc: Exception) -> JSONResponse:
    assert isinstance(exc, ApiError)
    return error_response(exc.status_code, exc.code, exc.message, exc.details)


async def _handle_http_exception(_request: Request, exc: Exception) -> JSONResponse:
    assert isinstance(exc, StarletteHTTPException)
    detail = exc.detail
    message = detail if isinstance(detail, str) else code_for_status(exc.status_code)
    details = None if isinstance(detail, str) else detail
    response = error_response(exc.status_code, code_for_status(exc.status_code), message, details)
    if exc.headers:
        response.headers.update(exc.headers)
    return response


async def _handle_validation_error(_request: Request, exc: Exception) -> JSONResponse:
    assert isinstance(exc, RequestValidationError)
    # ``exc.errors()`` may contain non-JSON values (e.g. a ValueError in ``ctx``);
    # ``jsonable_encoder`` is what FastAPI's own handler uses.
    return error_response(
        422, "validation_error", "Request validation failed.", jsonable_encoder(exc.errors())
    )


async def _handle_unexpected(_request: Request, _exc: Exception) -> JSONResponse:
    # Never leak internals. Starlette still re-raises so the error is logged/reported.
    return error_response(500, "internal_server_error", "Internal server error.")


def install_error_handlers(app: FastAPI) -> None:
    """Register the handlers that turn every exception into the envelope."""
    app.add_exception_handler(ApiError, _handle_api_error)
    app.add_exception_handler(StarletteHTTPException, _handle_http_exception)
    app.add_exception_handler(RequestValidationError, _handle_validation_error)
    app.add_exception_handler(Exception, _handle_unexpected)


# Attach to routers/apps so the OpenAPI document describes the envelope instead of
# FastAPI's default ``HTTPValidationError``.
ERROR_RESPONSES: dict[int | str, dict[str, Any]] = {
    422: {"model": ErrorEnvelope, "description": "Validation error"},
    "4XX": {"model": ErrorEnvelope, "description": "Client error"},
    "5XX": {"model": ErrorEnvelope, "description": "Server error"},
}
