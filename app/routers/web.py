from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from lesson_2.app.security.csrf import generate_csrf_token
from lesson_2.app.config import settings
import logging

router = APIRouter(tags=["web"], include_in_schema=False)
logger = logging.getLogger(__name__)
templates = Jinja2Templates(directory=str(settings.TEMPLATES_DIR))


def log_template_request(request: Request):
    """Логирование информации о запросе шаблона"""
    logger.info(
        f"Template request | Path: {request.url.path} | "
        f"Client: {request.client.host if request.client else 'unknown'} | "
        f"Method: {request.method}"
    )


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    try:
        log_template_request(request)
        response = templates.TemplateResponse(
            "index.html",
            {"request": request, "active_page": "home"}
        )
        logger.debug(f"Rendered index page | Status: {response.status_code}")
        return response
    except Exception as e:
        logger.error(
            f"Error rendering index template | Error: {str(e)}",
            exc_info=True
        )
        raise


@router.get("/login", response_class=HTMLResponse, name="web_login")
async def login_page(request: Request):
    try:
        log_template_request(request)
        csrf_token = generate_csrf_token()
        logger.debug("Generated CSRF token for login page")

        response = templates.TemplateResponse(
            "auth/login.html",
            {"request": request, "csrf_token": csrf_token}
        )
        logger.info(f"Rendered login page | Status: {response.status_code}")
        return response
    except Exception as e:
        logger.error(
            f"Error rendering login template | Error: {str(e)}",
            exc_info=True
        )
        raise


@router.get("/register", response_class=HTMLResponse, name="web_register")
async def register_page(request: Request):
    try:
        log_template_request(request)
        csrf_token = generate_csrf_token()
        logger.debug("Generated CSRF token for registration page")

        response = templates.TemplateResponse(
            "auth/register.html",
            {"request": request, "csrf_token": csrf_token}
        )
        logger.info(f"Rendered registration page | Status: {response.status_code}")
        return response
    except Exception as e:
        logger.error(
            f"Error rendering registration template | Error: {str(e)}",
            exc_info=True
        )
        raise


@router.get("/create-prediction", response_class=HTMLResponse)
async def create_prediction_page(request: Request):
    try:
        log_template_request(request)
        logger.debug("Accessing prediction creation page")

        response = templates.TemplateResponse(
            "predictions/create.html",
            {"request": request, "active_page": "create_prediction"}
        )
        logger.info(f"Rendered prediction creation page | Status: {response.status_code}")
        return response
    except Exception as e:
        logger.error(
            f"Error rendering prediction creation template | Error: {str(e)}",
            exc_info=True
        )
        raise


@router.get("/prediction/{prediction_id}", response_class=HTMLResponse)
async def prediction_detail(request: Request, prediction_id: int):
    try:
        log_template_request(request)
        logger.info(
            f"Accessing prediction detail | PredictionID: {prediction_id}"
        )

        response = templates.TemplateResponse(
            "predictions/detail.html",
            {
                "request": request,
                "active_page": "predictions",
                "prediction_id": prediction_id
            }
        )
        logger.debug(f"Rendered prediction detail page | PredictionID: {prediction_id}")
        return response
    except Exception as e:
        logger.error(f"Error rendering prediction detail template | "
            f"PredictionID: {prediction_id} | Error: {str(e)}",
            exc_info=True
        )
        raise

@router.get("/transactions", response_class=HTMLResponse)
async def transactions_history(request: Request):
    try:
        log_template_request(request)
        logger.debug("Accessing transactions history page")
        
        response = templates.TemplateResponse(
            "transactions/history.html",
            {"request": request, "active_page": "transactions"}
        )
        logger.info("Rendered transactions history page")
        return response
    except Exception as e:
        logger.error(
            f"Error rendering transactions history template | Error: {str(e)}",
            exc_info=True
        )
        raise
