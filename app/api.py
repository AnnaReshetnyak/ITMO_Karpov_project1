from fastapi import FastAPI
from app.routers import auth, users, predictions, balance
from database.database import init_db
import uvicorn

app = FastAPI()

app.include_router(home.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(predictions.router)
app.include_router(balance.router)


@app.on_event("startup")

def on_startup():
    init_db()

if __name__ == '__main__':
    uvicorn.run('api:app', host='0.0.0.0', port=8000, reload=True)
