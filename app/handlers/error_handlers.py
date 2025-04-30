from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.exceptions import RequestValidationError
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from starlette.exceptions import HTTPException as StarletteHTTPException
from typing import Union
import logging
from exceptions import InsufficientFundsError

# Инициализация логгера в начале файла
logger = logging.getLogger(__name__)
templates = Jinja2Templates(directory="app/view/templates")


async def insufficient_funds_handler(
        request: Request,
        exc: InsufficientFundsError
) -> Union[JSONResponse, HTMLResponse]:
    """Обработка ошибки недостатка средств"""
    logger.warning(
        f"Insufficient funds error: User {getattr(request.state, 'user_id', 'unknown')} | "
        f"Required: {exc.required_amount} | Available: {exc.balance} | "
        f"Endpoint: {request.url.path}"
    )

    context = {
        "request": request,
        "status_code": 402,
        "detail": f"Недостаточно средств. Текущий баланс: {exc.balance}",
        "balance": exc.balance
    }

    if "application/json" in request.headers.get("accept", ""):
        return JSONResponse(
            status_code=402,
            content=jsonable_encoder(context)
        )

    return templates.TemplateResponse(
        "errors/insufficient_funds.html",
        context,
        status_code=402
    )


async def http_exception_handler(
        request: Request,
        exc: StarletteHTTPException
) -> Union[JSONResponse, HTMLResponse]:
    """Обработка HTTP исключений"""
    log_level = logging.INFO if exc.status_code < 500 else logging.ERROR
    logger.log(
        log_level,
        f"HTTP Error {exc.status_code}: {exc.detail} | "
        f"Path: {request.url.path} | Method: {request.method} | "
        f"Client: {request.client.host if request.client else 'unknown'}"
    )

    context = {
        "request": request,
        "status_code": exc.status_code,
        "detail": exc.detail
    }

    if "application/json" in request.headers.get("accept", ""):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )

    return templates.TemplateResponse(
        "errors/error.html",
        context,
        status_code=exc.status_code
    )


async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError
) -> Union[JSONResponse, HTMLResponse]:
    """Обработка ошибок валидации"""
    logger.warning(
        f"Validation error: {exc.errors()} | "
        f"Path: {request.url.path} | "
        f"Parameters: {request.path_params} | "
        f"Client: {request.client.host if request.client else 'unknown'}"
    )

    if "application/json" in request.headers.get("accept", ""):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": jsonable_encoder(exc.errors())}
        )

    return templates.TemplateResponse(
        "errors/validation_error.html",
        {
            "request": request,
            "errors": exc.errors()
        },
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )


async def generic_exception_handler(
        request: Request,
        exc: Exception
) -> Union[JSONResponse, HTMLResponse]:
    """Обработка всех неожиданных исключений"""
    logger.error(
        f"Unhandled exception: {str(exc)} | "
        f"Path: {request.url.path} | "
        f"Method: {request.method} | "
        f"Client: {request.client.host if request.client else 'unknown'}",
        exc_info=True
    )

    if "application/json" in request.headers.get("accept", ""):
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal Server Error"}
        )

    return templates.TemplateResponse(
        "errors/500.html",
        {"request": request},
        status_code=500
    )


def register_error_handlers(app: FastAPI) -> None:
    """Регистрация обработчиков ошибок"""
    app.add_exception_handler(InsufficientFundsError, insufficient_funds_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)


