from datetime import datetime, timedelta
from typing import List
from models.foodHistory import FoodHistory
from config.db import foodHistoryDb, foodDb
from bson import ObjectId
from pymongo import DESCENDING

from schemas.history import FoodHistoryResponse
from services.food import find_foods_by_id

def find_last_week_accept_cluster(user_id: str):
  last_week = datetime.utcnow() - timedelta(days=7)
  cluster_ids = foodHistoryDb.find({ 'userId': ObjectId(user_id),'isSuccess': True, 'createAt': {"$gte": last_week}}).distinct('clusterId')

  return cluster_ids

def find_month_cluster(user_id: str, exclude_clusters: List[int]= []):
  last_month = datetime.utcnow() - timedelta(days=30)
  pipeline = [
    {"$match": {
      'userId': ObjectId(user_id), 
      'createAt': {"$gte": last_month}, 
      'clusterId': {'$nin': exclude_clusters}
    }},
    {"$group": {"_id": "$clusterId", "accept": {"$sum": {"$cond": [{"$eq": ["$isSuccess", True]}, 1, 0]}}, "reject": {"$sum": {"$cond": [{"$eq": ["$isSuccess", False]}, 1, 0]}}}}
  ]

  cluster_scores = foodHistoryDb.aggregate(pipeline)

  return list(cluster_scores)

def add_log_food_history(user_id: str,food_id: str, is_success: bool,predict=True):
  food = foodDb.find_one({'_id': ObjectId(food_id)})
  new_log = FoodHistory(userId=user_id,foodId=food_id,isSuccess=is_success,clusterId=food['clusterId'],random=predict)

  foodHistoryDb.insert_one(new_log.dict(by_alias=True))
  
def find_log_food_history(user_id: str,start: int = 0,limit: int = 30):
  food_history_log = foodHistoryDb.find({'userId': ObjectId(user_id)}).sort('createAt',DESCENDING).skip(start).limit(limit)

  food_history_log = list(food_history_log)

  food_id_list = [history_log["foodId"] for history_log in food_history_log]

  food = find_foods_by_id(food_id_list)

  log_with_food_info = [{**history_log,'food': food[history_log["foodId"]]} for history_log in food_history_log]

  return FoodHistoryResponse(start=start+limit,limit=limit,data=log_with_food_info)
