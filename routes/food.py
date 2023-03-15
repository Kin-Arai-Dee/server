from code import interact
from fastapi import APIRouter, Request
from schemas.food import FoodNameResponse,TagListResponse, IngredientListResponse, TopIngredientListResponse
from schemas.prediction import ListFoodResponse
from schemas.utils import ResultResponse2
from services.food import get_all_categories, get_all_food_name, get_all_ingredients, get_all_methods, get_all_tags, get_ramdom_unvoted_food, get_top_food_by_tag_id, ingredient_user_eat, top_ten_food, user_top_food_list

from services.foodFrequency import set_food_interact
food = APIRouter()

@food.get('/ingredients', response_model=IngredientListResponse)
async def get_all_ingredients_list():
  return get_all_ingredients()

@food.get('/tags', response_model=TagListResponse)
async def get_all_tags_list():
  return get_all_tags()

@food.get('/methods', response_model=TagListResponse)
async def get_all_methods_list():
  return get_all_methods()

@food.get('/categories', response_model=TagListResponse)
async def get_all_categories_list():
  return get_all_categories()

@food.get('/food-list', response_model=FoodNameResponse)
async def get_all_food_name_list():
  return get_all_food_name()

@food.get('/top-food/{tag_id}', response_model=FoodNameResponse)
async def get_all_food_name_list(tag_id: str):
  return get_top_food_by_tag_id(tag_id)

@food.get('/unvoted-food-list', response_model=FoodNameResponse)
async def get_ramdom_unvoted_food_list(request: Request,size: int = 30):
  return get_ramdom_unvoted_food(request.state.user.id,size)

# @food.get('/favorite-food',response_model=ListFoodResponse)
# async def get_user_favorite_food(request: Request):
#   return favorite_food(request.state.user.id)

@food.get('/top-food',response_model=ListFoodResponse)
async def get_top_food():
  return top_ten_food()

# @food.patch('/never-show/{food_id}')
# async def never_show_food(request: Request, food_id: str):
#   return set_not_show(request.state.user.id, food_id)

@food.patch('/interact/{food_id}',response_model=ResultResponse2)
async def update_food_interact(request: Request,food_id: str,interact: int,clusterId: int):
  return set_food_interact(request.state.user.id,food_id,interact,clusterId)

@food.get('/top-ingredients', response_model=TopIngredientListResponse)
async def find_user_top_ingredient(request: Request):
  return ingredient_user_eat(request.state.user.id)

@food.get('/top-user-food', response_model=ListFoodResponse)
async def top_food_user_eat(request: Request):
  return user_top_food_list(request.state.user.id)