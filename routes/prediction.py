from fastapi import APIRouter, Request
from schemas.prediction import PredictionSubmitRequest, ListFoodResponse
from schemas.utils import ResultResponse

from services.prediction import prediction_food, submit_prediction_result

prediction = APIRouter()

@prediction.get('/food', response_model=ListFoodResponse)
async def perdiction_food_from_model(request: Request, force: bool):
  return await prediction_food(request.state.user.id,force)

@prediction.post('/submit/{food_id}', response_model=ResultResponse)
async def submit_prediction_food_result(request: Request,food_id: str, result: PredictionSubmitRequest):
  return await submit_prediction_result(request.state.user.id,food_id, result.impress)
