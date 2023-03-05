from datetime import datetime
from typing import List
from venv import create
from config.db import foodFreqDb, userStatDb
from bson import ObjectId
from pymongo import DESCENDING, UpdateOne

from fastapi import HTTPException, status
from models.foodFrequency import FoodFrequency, FoodFrequencyDefault

FOOD_FREQUENCY_NOT_FOUND = HTTPException(
		status_code=status.HTTP_404_NOT_FOUND,
		detail="Food Frequency not found",
)

def update_user_stat(user_id: str, cluster_id: int,score: int):
  update_info = {}
  create_info = {}
  if score < 0 :
    update_info['dislike'] = 1
    create_info['like'] = 0
  elif score > 0:
    update_info['like'] = score
    create_info['dislike'] = 0

  userStatDb.update_one({'userId': ObjectId(user_id), 'clusterId': cluster_id}, 
    {
      '$set': {'updateAt': datetime.now()},
      '$inc': update_info,
      '$setOnInsert': {'createAt': datetime.now(), **create_info}
    }, 
    upsert=True)

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

def add_frequency(id: ObjectId,success:bool=True):
  increateData = {}

  if success: 
    increateData["successCount"] = 1
  else:
    increateData["failCount"] = 1  
  
  foodFreqDb.update_one({'_id': id } , {     
    '$set': { 'updateAt': datetime.now()},
    '$inc': increateData
  })

# def toggle_favorite_food(food_freq: FoodFrequency):
#   foodFreqDb.update_one({'_id':food_freq.id}, {
#     '$set': { 
#       'isFavorite':  not food_freq.IsFavorite,
#       'updateAt': datetime.now()},
#   })

# def toggle_not_show(food_freq: FoodFrequency):
#   foodFreqDb.update_one({'_id':food_freq.id},{
#     '$set': { 
#       'isNeverShow':  not food_freq.isNeverShow,
#       'updateAt': datetime.now()},
#   })

#   return {
#     "detail": f"set food never show to be {not food_freq.isNeverShow}"
#   }

def ban_food_by_id(user_id:str,food_id_list: List[str]):
  update_food_ban = []

  for food_id in food_id_list:
    update_food_ban.append(UpdateOne({
      'foodId': food_id,
      'userId': user_id,
    }, {
      '$set': {
        'updateAt': datetime.now(),
        'isBan': True,
      },
      '$setOnInsert': FoodFrequencyDefault().dict()
      }, upsert=True))

  foodFreqDb.bulk_write(update_food_ban)

def find_top_ten_food_id():
  top_freq_food = foodFreqDb.aggregate([
    {
      '$group': {
        '_id': '$foodId',
        'successCount': {'$sum': '$successCount'}
      }
    },
    {
      '$sort': {'successCount': DESCENDING}
    },
    {
      '$limit': 10
    },
  ])

  return [food["_id"] for food in top_freq_food]

def find_top_user_food_id(user_id: str):
  top_freq_food_id = foodFreqDb.find({'userId': ObjectId(user_id)}).sort('successCount',DESCENDING).distinct('foodId')

  return top_freq_food_id

# def find_favorite_food_id(user_id: str):
#   favorite_food_id = foodFreqDb.find({ 'userId': ObjectId(user_id), 'isFavorite': True }).distinct('foodId')
#   return favorite_food_id

def get_all_ban_food_id(user_id: str):
  ban_food_id = foodFreqDb.find({
    'userId': ObjectId(user_id),
    '$or':[
      { 
        'isBan': True,
      },{ 
        'isNeverShow': True, 
      }]
  }).distinct('foodId')

  return ban_food_id

# def set_not_show(user_id: str,food_id: str):
#   foodFreq = create_or_find_food_frequency_db(user_id,food_id)
#   return toggle_not_show(foodFreq)

def set_food_interact(user_id:str,food_id: str, interact: int, cluster_id: int):
  food_freq = create_or_find_food_frequency_db(user_id,food_id)

  foodFreqDb.update_one({"_id": food_freq.id}, {
    "$set": {
      'updateAt': datetime.now(),
      "interact": interact
    }
  })

  update_user_stat(user_id,cluster_id, interact)

  return {
    "detail": "update success"
  }


def get_all_voted_food_id(user_id: str):
  food_freq_list_id = foodFreqDb.find({
    'userId': ObjectId(user_id),
    'interact': { '$ne': 0}
    }
  ).distinct('foodId')

  return food_freq_list_id

def find_all_user_eaten_food_id(user_id: str):
  food_freq_list_id = foodFreqDb.find({
    'userId': ObjectId(user_id),
    }
  ).distinct('foodId')

  return food_freq_list_id

def find_all_most_user_eaten(user_id: str):
  food_freq_list_id = foodFreqDb.find({
    'userId': ObjectId(user_id),
    }
  ).sort('successCount',DESCENDING)

  return [d['foodId'] for d in food_freq_list_id]

