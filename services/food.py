from typing import List
from schemas.food import FoodName, FoodNameResponse, ListFoodResponse
from services.foodFrequency import find_favorite_food_id, find_top_ten_food_id
from config.db import foodDb

def top_ten_food():
  top_food_id = find_top_ten_food_id()

  top_food = foodDb.find({ '_id': {'$in' : top_food_id}})

  return ListFoodResponse(data=list(top_food))

def favorite_food(user_id: str):
  favorite_food_id = find_favorite_food_id(user_id)

  favorite_food = foodDb.find({ '_id': {'$in' : favorite_food_id}})

  return ListFoodResponse(data=list(favorite_food))

def get_all_food_name():
  return FoodNameResponse(data=[list(foodDb.find())])

def get_food_id_by_ingredient(ingredients: List[str]):
  food_list = foodDb.find({
    '$or': [{
      'ingredient1' : { '$in': ingredients}
    },{
      'ingredient2' : { '$in': ingredients}
    }
  ]})

  return [food["_id"] for food in food_list]
