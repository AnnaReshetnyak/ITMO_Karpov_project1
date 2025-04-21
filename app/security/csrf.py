import secrets
from fastapi import Request, Depends
from typing import Optional


def generate_csrf_token(request: Request) -> str:

    # Генерируем новый токен
    csrf_token = secrets.token_urlsafe(32)

    # Сохраняем в сессии
    request.session["csrf_token"] = csrf_token

    return csrf_token


async def validate_csrf_token(
        request: Request,
        submitted_token: Optional[str] = None
) -> bool:

    session_token = request.session.get("csrf_token")

    if not session_token or not submitted_token:
        return False

    return secrets.compare_digest(session_token, submitted_token)
