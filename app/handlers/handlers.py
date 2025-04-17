from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.exceptions import RequestValidationError
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from starlette.exceptions import HTTPException as StarletteHTTPException
from typing import Union
import logging
from lesson_2.app.exceptions import InsufficientFundsError


async def insufficient_funds_handler(
        request: Request,
        exc: InsufficientFundsError
) -> Union[JSONResponse, HTMLResponse]:
    """Обработка ошибки недостатка средств"""
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


def register_error_handlers(app: FastAPI) -> None:
    app.add_exception_handler(InsufficientFundsError, insufficient_funds_handler)

logger = logging.getLogger(__name__)
templates = Jinja2Templates(directory="app/web/templates")


async def http_exception_handler(
        request: Request,
        exc: StarletteHTTPException
) -> Union[JSONResponse, HTMLResponse]:
    """Обработка HTTP исключений"""
    context = {
        "request": request,
        "status_code": exc.status_code,
        "detail": exc.detail
    }

    # Для API запросов
    if "application/json" in request.headers.get("accept", ""):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )

    # Для веб-интерфейса
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
    logger.error(f"Validation error: {exc.errors()}")

    # Для API
    if "application/json" in request.headers.get("accept", ""):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": jsonable_encoder(exc.errors())}
        )

    # Для веб-интерфейса
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
    logger.critical(f"Unhandled exception: {str(exc)}", exc_info=True)

    # Для API
    if "application/json" in request.headers.get("accept", ""):
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal Server Error"}
        )

    # Для веб-интерфейса
    return templates.TemplateResponse(
        "errors/500.html",
        {"request": request},
        status_code=500
    )


def register_error_handlers(app: FastAPI) -> None:
    """Регистрация обработчиков ошибок"""
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)
