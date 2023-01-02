from fastapi import APIRouter, Depends, Request

from services.food import favorite_food, get_all_food_name, top_ten_food

food = APIRouter()

@food.get('/food-list')
async def get_all_food_name_list():
  return get_all_food_name()

@food.get('/favorite-food')
async def get_user_favorite_food(request: Request):
  return favorite_food(request.state.user.id)

@food.get('/top-food')
async def get_top_food():
  return top_ten_food()
