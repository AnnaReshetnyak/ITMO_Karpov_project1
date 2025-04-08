from fastapi import APIRouter, Body, HTTPException

transaction_router = APIRouter()

transactions = []



@transaction_router.get("/{transaction_id}")
async def get_transaction(transaction_id:int):
    transaction=next((transaction for transaction in transactions if transaction ["id"] == transaction_id), None)
    if transaction is None:
        return {"message": "transaction not found"}
    return transaction


@transaction_router.post("/")
async def create_transaction(transaction:dict):
    transactions.append(transaction)
    return{"message": "transaction created successfully", "transaction": transaction}
