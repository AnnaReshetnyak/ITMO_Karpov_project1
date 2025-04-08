from fastapi import APIRouter

from app.schemas import  BalanceBase, BalanceOperation



balance_router = APIRouter(tags=["Balance"],
                           responses={404: {"description": "Not found"}},
                           prefix="/balance")

@balance_router.get("/balance")
async def get_balance(operation: BalanceBase):

    return {"message": "Operation processed", "amount": operation.amount}



@balance_router.post("/balance")
async def update_balance(operation: BalanceOperation):
    return {"message": "Operation processed", "amount": operation.amount}
