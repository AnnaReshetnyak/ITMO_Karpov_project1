from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pathlib import Path
from app.config import settings

router = APIRouter(tags=["web"], include_in_schema=False)

# Инициализация шаблонов с учетом новой структуры
templates = Jinja2Templates(directory=str(settings.TEMPLATES_DIR))

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "active_page": "home"}
    )

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(
        "auth/login.html",
        {"request": request, "active_page": "login"}
    )

@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse(
        "auth/register.html",
        {"request": request, "active_page": "register"}
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
