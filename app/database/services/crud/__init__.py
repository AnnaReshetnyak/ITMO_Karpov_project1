from app.database.services.crud.user_crud import UserCRUD
from app.database.services.crud.balance_crud import BalanceCRUD
from app.database.services.crud.transaction_crud import TransactionCRUD
from app.database.services.crud.transaction_history_crud import TransactionHistoryCRUD
from app.database.services.crud.mlmodel_crud import MLModelCRUD
from app.database.services.crud.mltask_crud import MLTaskCRUD
from app.database.services.crud.prediction_history import (PredictionHistoryCRUD)

all = [
    "UserCRUD",
    "BalanceCRUD",
    "TransactionCRUD",
    "TransactionHistoryCRUD",
    "MLModelCRUD",
    "MLTaskCRUD",
    "PredictionHistoryCRUD"
]
