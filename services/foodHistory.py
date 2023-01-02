from models.foodHistory import FoodHistory
from config.db import foodHistoryDb
from bson import ObjectId
from pymongo import DESCENDING

from schemas.history import FoodHistoryResponse

def add_log_food_history(user_id: str,food_id: str, is_success: bool):
  new_log = FoodHistory(userId=user_id,foodId=food_id,isSuccess=is_success)

  foodHistoryDb.insert_one(new_log.dict(by_alias=True))
  
def find_log_food_history(user_id: str,start: int = 0,limit: int = 30):
  food_history_log = foodHistoryDb.find({'userId': ObjectId(user_id)}).sort('createAt',DESCENDING).skip(start).limit(limit)

  return FoodHistoryResponse(start=start+limit,limit=limit,foodHistory=list(food_history_log))
