from datetime import datetime
from typing import List
from config.db import foodFreqDb
from bson import ObjectId
from pymongo import DESCENDING

from fastapi import HTTPException, status
from models.foodFrequency import FoodFrequency

FOOD_FREQUENCY_NOT_FOUND = HTTPException(
		status_code=status.HTTP_404_NOT_FOUND,
		detail="Food Frequency not found",
)

def find_food_frequency_db(user_id: str, food_id: str, must_found: bool =True):
  food_freq = foodFreqDb.find_one({'userId': ObjectId(user_id), 'foodId': ObjectId(food_id)})

  if food_freq:
    return FoodFrequency(**food_freq)
  elif must_found:
    raise FOOD_FREQUENCY_NOT_FOUND
  else:
    return False

def create_or_find_food_frequency_db(user_id: str, food_id: str) -> FoodFrequency:
  food_freq = find_food_frequency_db(user_id,food_id,must_found=False)

  if(food_freq):
    return food_freq
  
  new_food_freq = FoodFrequency(userId=user_id,foodId=food_id)
  foodFreqDb.insert_one(new_food_freq.dict(by_alias=True))
  return new_food_freq

def create_new_foods_frequency_db(user_id: str, food_id_list: List[str],defaultValue: dict) -> FoodFrequency:
  new_food_freq_list = [FoodFrequency(userId=user_id,foodId=id,**defaultValue).dict(by_alias=True) for id in food_id_list]

  foodFreqDb.insert_many(new_food_freq_list)

def add_frequency(id: ObjectId,success:bool=True,predict:bool=True):
  increateData = {
    'frequency' : 1
  }

  if success: 
    increateData["successCount"] = 1
    if predict:
      increateData["successRandomCount"] = 1
  else:
    increateData["failCount"] = 1  
  
  foodFreqDb.update_one({'_id': id } , {     
    '$set': { 'updateAt': datetime.now()},
    '$inc': increateData
  })

def toggle_favorite_food(food_freq: FoodFrequency):
  foodFreqDb.update_one({'_id':food_freq.id}, {
    '$set': { 
      'isFavorite':  not food_freq.IsFavorite,
      'updateAt': datetime.now()},
  })

def toggle_not_show(food_freq: FoodFrequency):
  foodFreqDb.update_one({'_id':food_freq.id},{
    '$set': { 
      'isNeverShow':  not food_freq.isNeverShow,
      'updateAt': datetime.now()},
  })

  return {
    "detail": f"set food never show to be {not food_freq.isNeverShow}"
  }

def ban_food_by_id(user_id:str,food_id_list: List[str]):
  food_freq_id_list = [create_or_find_food_frequency_db(user_id,food_id).id for food_id in food_id_list]

  foodFreqDb.update_many({ 
    '_id': { 
      '$in': food_freq_id_list
    }}, { '$set' : {'isBan': True}})

def find_top_ten_food_id():
  top_freq_food = foodFreqDb.find().sort('frequency',DESCENDING).limit(10)
  return [food["foodId"] for food in top_freq_food]

def find_favorite_food_id(user_id: str):
  favorite_food = foodFreqDb.find({ 'userId': ObjectId(user_id), 'isFavorite': True })
  return [food["foodId"] for food in favorite_food]

def get_all_ban_food_id(user_id: str):
  ban_food = foodFreqDb.find({
    'userId': ObjectId(user_id),
    '$or':[
      { 
        'isBan': True,
      },{ 
        'isNeverShow': True, 
      }]
  })

  return [food["foodId"] for food in ban_food]

def set_not_show(user_id: str,food_id: str):
  foodFreq = create_or_find_food_frequency_db(user_id,food_id)
  return toggle_not_show(foodFreq)
