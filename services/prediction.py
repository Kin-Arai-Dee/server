from config.db import foodDb
from schemas.prediction import ListFoodResponse

from services.foodFrequency import add_frequency, create_or_find_food_frequency_db, get_all_ban_food_id
from services.foodHistory import add_log_food_history

async def prediction_food(user_id: str):
  # TODO: run valid ml model here
  ban_id_list = get_all_ban_food_id(user_id)

  food = foodDb.aggregate([
    {'$match': { '_id': { '$nin': ban_id_list}}},
    {'$sample': {'size': 3}}
  ])
  
  return ListFoodResponse(data=list(food))

async def submit_prediction_result(userId: str,foodId: str, impress: bool):
  food_freq = create_or_find_food_frequency_db(userId,foodId)
  add_frequency(food_freq.id,success=impress)
  add_log_food_history(userId,foodId,is_success=impress)

  return {
    "result": "add frequency and log successfully"
  }
