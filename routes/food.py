from fastapi import APIRouter, Request
from schemas.food import FoodNameResponse, ListFoodResponse

from services.food import favorite_food, get_all_food_name, top_ten_food
from services.foodFrequency import set_not_show

food = APIRouter()

@food.get('/food-list', response_model=FoodNameResponse)
async def get_all_food_name_list():
  return get_all_food_name()

@food.get('/favorite-food',response_model=ListFoodResponse)
async def get_user_favorite_food(request: Request):
  return favorite_food(request.state.user.id)

@food.get('/top-food',response_model=ListFoodResponse)
async def get_top_food():
  return top_ten_food()

@food.patch('/never-show/{food_id}')
async def never_show_food(request: Request, food_id: str):
  return set_not_show(request.state.user.id, food_id)
