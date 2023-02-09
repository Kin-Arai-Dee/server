from code import interact
from fastapi import APIRouter, Request
from schemas.food import FoodNameResponse
from schemas.prediction import ListFoodResponse

from services.food import favorite_food, get_all_food_name, get_ramdom_unvoted_food, top_ten_food
from services.foodFrequency import set_food_interact, set_not_show
from config.db import foodDb
food = APIRouter()

@food.get('/food-list', response_model=FoodNameResponse)
async def get_all_food_name_list():
  return get_all_food_name()

@food.get('/unvoted-food-list', response_model=FoodNameResponse)
async def get_ramdom_unvoted_food_list(request: Request,size: int = 30):
  return get_ramdom_unvoted_food(request.state.user.id,size)

@food.get('/favorite-food',response_model=ListFoodResponse)
async def get_user_favorite_food(request: Request):
  return favorite_food(request.state.user.id)

@food.get('/top-food',response_model=ListFoodResponse)
async def get_top_food():
  return top_ten_food()

@food.patch('/never-show/{food_id}')
async def never_show_food(request: Request, food_id: str):
  return set_not_show(request.state.user.id, food_id)

@food.patch('/interact/{food_id}')
async def update_food_interact(request: Request,food_id: str,interact: int):
  return set_food_interact(request.state.user.id,food_id,interact)