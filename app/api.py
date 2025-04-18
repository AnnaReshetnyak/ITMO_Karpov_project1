from fastapi import FastAPI, Request
from lesson_2.app.routers import home2, auth, users, predictions, balance, routes, web
from database.database import init_db
import uvicorn
import os
from fastapi.staticfiles import StaticFiles


app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"Request received: {request.method} {request.url.path}")
    response = await call_next(request)
    print(f"Response status: {response.status_code}")
    return response


app.include_router(home.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(predictions.router)
app.include_router(balance.router)
app.include_router(web.router)


@app.on_event("startup")

def on_startup():
    init_db()

if __name__ == '__main__':
    uvicorn.run('api:app', host='0.0.0.0', port=8000, reload=True)
