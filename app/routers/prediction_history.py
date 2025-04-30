from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from database.services.crud.prediction_history import PredictionHistoryCRUD
from database.database import get_session
from schemas import PredictionHistoryCreate, PredictionHistoryOut

prediction_history_router = APIRouter()

@prediction_history_router.post("/predictions/", response_model=PredictionHistoryOut)
def create_prediction(
    prediction_data: PredictionHistoryCreate,
    session: Session = Depends(get_session)
):
    crud = PredictionHistoryCRUD(session)
    return crud.create(prediction_data)

@prediction_history_router.get("/predictions/{prediction_id}/feedback")
def add_prediction_feedback(
    prediction_id: int,
    feedback: dict,
    session: Session = Depends(get_session)
):
    crud = PredictionHistoryCRUD(session)
    updated = crud.add_feedback(prediction_id, feedback)
    if not updated:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return updated
