from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from lesson_2.app.security.csrf import generate_csrf_token
from lesson_2.app.config import settings

router = APIRouter(tags=["web"], include_in_schema=False)

# Инициализация шаблонов с учетом новой структуры
templates = Jinja2Templates(directory=str(settings.TEMPLATES_DIR))

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "active_page": "home"}
    )



@router.get("/login", response_class=HTMLResponse, name="web_login")
async def login_page(request: Request):
    return templates.TemplateResponse(
        "auth/login.html",
        {
            "request": request,
            "csrf_token": generate_csrf_token()
        }
    )

@router.get("/register", response_class=HTMLResponse, name="web_register")
async def register_page(request: Request):
    return templates.TemplateResponse(
        "auth/register.html",
        {
            "request": request,
            "csrf_token": generate_csrf_token()
        }
    )

@router.get("/create-prediction", response_class=HTMLResponse)
async def create_prediction_page(request: Request):
    return templates.TemplateResponse(
        "predictions/create.html",
        {"request": request, "active_page": "create_prediction"}
    )

@router.get("/prediction/{prediction_id}", response_class=HTMLResponse)
async def prediction_detail(request: Request, prediction_id: int):
    return templates.TemplateResponse(
        "predictions/detail.html",
        {
            "request": request,
            "active_page": "predictions",
            "prediction_id": prediction_id
        }
    )

@router.get("/transactions", response_class=HTMLResponse)
async def transactions_history(request: Request):
    return templates.TemplateResponse(
        "transactions/history.html",
        {"request": request, "active_page": "transactions"}
    )

@router.get("/transactions", response_class=HTMLResponse)
async def transactions_history(request: Request):
    return templates.TemplateResponse(
        "transactions/history.html",
        {"request": request, "active_page": "transactions"}
    )
