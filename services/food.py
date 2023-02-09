from typing import List
from schemas.food import FoodNameResponse
from services.foodFrequency import find_favorite_food_id, find_top_ten_food_id, get_all_voted_food_id
from config.db import foodDb
from schemas.prediction import ListFoodResponse
from bson import ObjectId

def top_ten_food():
  top_food_id = find_top_ten_food_id()

  top_food = foodDb.find({ '_id': {'$in' : top_food_id}})

  return ListFoodResponse(data=list(top_food))

def favorite_food(user_id: str):
  favorite_food_id = find_favorite_food_id(user_id)

  favorite_food = foodDb.find({ '_id': {'$in' : favorite_food_id}})

  return ListFoodResponse(data=list(favorite_food))

def get_all_food_name():
  return FoodNameResponse(data=list(foodDb.find()))

def get_ramdom_unvoted_food(user_id: str,size: int):
  food_id_list = get_all_voted_food_id(user_id)

  return FoodNameResponse(data=list(foodDb.aggregate([
    {'$match': { '_id': { '$nin': food_id_list}}},
    {'$sample': {'size': size}}
  ])))

def get_food_id_by_ingredient(ingredients: List[str]):
  food_list = foodDb.find({
    '$or': [{
      'ingredient1' : { '$in': ingredients}
    },{
      'ingredient2' : { '$in': ingredients}
    }
  ]})

  return [food["_id"] for food in food_list]

def find_foods_by_id(food_id_list: List[ObjectId]):
  food_list = foodDb.find({
    '_id': { '$in': food_id_list}
  })

  return  {food_list['_id']:food_list for food_list in food_list}

