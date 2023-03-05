from typing import List

from pymongo import DESCENDING
from schemas.food import FoodNameResponse, IngredientListResponse, TopIngredientListResponse
from services.foodFrequency import find_all_most_user_eaten, find_top_ten_food_id, find_top_user_food_id, get_all_voted_food_id
from config.db import foodDb, ingredientDb, tagDb, methodDb, categoryDb, foodFreqDb
from schemas.prediction import ListFoodResponse
from bson import ObjectId

def get_user_food_pipeline(user_id: str, query: dict={}):
  return [{
  '$match': { 'userId': ObjectId(user_id), **query},
  }, {
    '$lookup': {
      'from': "Food",
      'localField': "foodId",
      'foreignField': "_id",
      'as': "food"
    }
  },{
  '$replaceRoot': { 'newRoot': { '$arrayElemAt': [ "$food", 0 ] } }
  }
]

def find_by_order(order_ids: List[str]):
  m = { "$match" : { "_id" : { "$in" : order_ids } } }
  a = { "$addFields" : { "__order" : { "$indexOfArray" : [ order_ids, "$_id" ] } } }
  s = { "$sort" : { "__order" : 1 } }
  
  top_food = foodDb.aggregate([m,a,s])

  return list(top_food)

def get_all_ingredients():
  return IngredientListResponse(data=list(ingredientDb.find()))

def get_all_tags():
  return IngredientListResponse(data=list(tagDb.find()))

def get_all_methods():
  return IngredientListResponse(data=list(methodDb.find()))

def get_all_categories():
  return IngredientListResponse(data=list(categoryDb.find()))

def top_ten_food():
  top_food_id = find_top_ten_food_id()

  top_food = find_by_order(top_food_id)
  return ListFoodResponse(data=list(top_food))

def top_user_food(user_id: str):
  top_food_id = find_top_user_food_id(user_id)

  top_food = foodDb.find({ '_id': {'$in' : top_food_id}})

  return ListFoodResponse(data=list(top_food))

# def favorite_food(user_id: str):
#   favorite_food_id = find_favorite_food_id(user_id)

#   favorite_food = foodDb.find({ '_id': {'$in' : favorite_food_id}})

#   return ListFoodResponse(data=list(favorite_food))

def get_all_food_name():
  all_food = list(foodDb.find())
  return FoodNameResponse(data=all_food)

def get_ramdom_unvoted_food(user_id: str,size: int):
  food_id_list = get_all_voted_food_id(user_id)

  unvoted_foods = foodDb.aggregate([
    {'$match': {'_id': {'$nin': food_id_list}}},
    {'$sample':{'size':1000}},
    { '$group': { '_id': "$clusterId", 'docs': { '$push': "$$ROOT" } } },
    { 
      '$project': { 
        'docs': { 
          '$slice': [ 
            "$docs", 0, { '$min': [ { '$size': "$docs" }, 3 ]}
          ] 
        } 
      }
    },
    { '$unwind': "$docs" },
    { '$replaceRoot': { 'newRoot': "$docs" } },
    { '$sample': {'size':size} }
  ])

  return FoodNameResponse(data=list(unvoted_foods))

def get_food_id_by_ingredient(ingredient_ids: List[str]):
  ingredient_ids = [ObjectId(id) for id in ingredient_ids]
  food_list_id = foodDb.find({
    'ingredientIds' : { '$all': ingredient_ids}
  }).distinct('_id')

  return food_list_id

def find_foods_by_id(food_id_list: List[ObjectId]):
  food_list = foodDb.find({
    '_id': { '$in': food_id_list}
  })

  return  {food_list['_id']:food_list for food_list in food_list}

def user_top_food_list(user_id: str):
  food_id = find_all_most_user_eaten(user_id)
  top_food = find_by_order(food_id)
  return ListFoodResponse(data=list(top_food))

def ingredient_user_eat(user_id: str,top_count: int = 5):
  pipeline = get_user_food_pipeline(user_id, {
    'successCount': { '$gt': 0}
  }) + [
  {
    '$lookup': {
      'from': "ingredient",
      'localField': "ingredientIds",
      'foreignField': "_id",
      'as': "ingredient"
    }
  },
  {
    '$unwind': "$ingredient"
  },
  {
    '$group': {
      '_id': "$ingredient._id",
      'ingredientName': { '$first' :"$ingredient.ingredientName"},
      'nutrient': {'$first' :'$ingredient.nutrient'},
      'count': { '$sum': 1 },
      }
    },
    {
      '$sort': { 'count': DESCENDING}
    },
    {
      '$group': {
        '_id': '$nutrient',
        'ingredient': {'$push': '$$ROOT'}
      }
    },
     { 
      '$project': { 
        'ingredient': { 
          '$slice': [ 
            "$ingredient", 0, { '$min': [ { '$size': "$ingredient" }, top_count ]}
          ] 
        } 
      }
    },
  ]

  ingredients = list(foodFreqDb.aggregate(pipeline))

  map_ingredients = {ingredient['_id']:ingredient['ingredient'] for ingredient in ingredients}

  return TopIngredientListResponse(**map_ingredients)
