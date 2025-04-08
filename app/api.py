from fastapi import FastAPI
from app.routers.home import home_router
from app.routers.user import user_router
from app.routers.balance import balance_router
from app.routers.prediction_history import prediction_history_router
from app.routers.mltask import mltask_router
from database.database import init_db
import uvicorn

app = FastAPI()

app.include_router(home_router)
app.include_router(user_router, prefix='/user')
app.include_router(balance_router, prefix='/balance')
app.include_router(mltask_router, prefix='/mltask')
app.include_router(prediction_history_router, prefix='/prediction_history')

@app("startup")
def on_startup():
    init_db()

if __name__ == '__main__':
    uvicorn.run('api:app', host='0.0.0.0', port=8000, reload=True)
