from database.services.crud.user_crud import UserCRUD
from database.services.crud.balance_crud import BalanceCRUD
from database.services.crud.transaction_crud import TransactionCRUD
from database.services.crud.transaction_history_crud import TransactionHistoryCRUD
from database.services.crud.mlmodel_crud import MLModelCRUD
from database.services.crud.mltask_crud import MLTaskCRUD


all = [
    "UserCRUD",
    "BalanceCRUD",
    "TransactionCRUD",
    "TransactionHistoryCRUD",
    "MLModelCRUD",
    "MLTaskCRUD",
]
