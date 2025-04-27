from lesson_2.app.routers import home2, auth, users, predictions, balance, routes, web
from lesson_2.app.database.database import init_db
import uvicorn
import os
from fastapi.staticfiles import StaticFiles
import logging
import logging.config
from logging.handlers import RotatingFileHandler
from fastapi import FastAPI, Request
from uuid import uuid4
from fastapi.middleware.cors import CORSMiddleware

os.makedirs("logs", exist_ok=True)

app = FastAPI(title="ML Prediction Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Конфигурация логгера должна быть ПЕРВОЙ перед созданием приложения
logging.config.dictConfig({
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] [%(name)s] [request_id:%(request_id)s] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard"
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/app.log",
            "maxBytes": 10 * 1024 * 1024,
            "backupCount": 5,
            "formatter": "standard",
            "encoding": "utf-8"
        },
        # Добавляем новый обработчик для БД
        "db_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/database.log",
            "maxBytes": 10 * 1024 * 1024,
            "backupCount": 3,
            "formatter": "standard",
            "encoding": "utf-8"
        }
    },
    "loggers": {
        "app": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False
        },
        # Добавляем новые логгеры
        "sqlalchemy": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False
        },
        "database": {
            "handlers": ["db_file"],
            "level": "DEBUG",
            "propagate": False
        }
    }
})



# Middleware должен быть объявлен до регистрации роутеров
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    """Добавляет уникальный ID к каждому запросу"""
    request_id = str(uuid4())
    request.state.request_id = request_id
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Логирование входящих запросов и ответов"""
    logger = logging.getLogger("app")
    request_id = request.state.request_id

    # Форматируем сообщение с request_id
    extra = {"request_id": request_id}

    logger.info(
        "Incoming request: %s %s",
        request.method,
        request.url.path,
        extra=extra
    )

    try:
        response = await call_next(request)
    except Exception as e:
        logger.error(
            "Request error: %s",
            str(e),
            exc_info=True,
            extra=extra
        )
        raise

    logger.info(
        "Response: status=%d | client=%s | path=%s",
        response.status_code,
        request.client.host if request.client else "unknown",
        request.url.path,
        extra=extra
    )

    return response


# Регистрация роутеров
app.include_router(home2.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(predictions.router)
app.include_router(balance.router)
app.include_router(web.router)


# Инициализация БД
@app.on_event("startup")
async def on_startup():
    await init_db()



if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        reload=True,
        # Логирование сервера тоже можно настроить
        log_config=None  # Используем свою конфигурацию
    )


