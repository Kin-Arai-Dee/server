from typing import List
from fastapi import HTTPException, status

from bson import ObjectId
from config.db import foodDb, userStatDb
from schemas.prediction import ListFoodResponse

from services.foodFrequency import add_frequency, create_or_find_food_frequency_db, get_all_ban_food_id
from services.foodHistory import add_log_food_history, find_last_week_accept_cluster, find_month_cluster

NUM_OF_CLUSTER = 48
ACCEPT_WEIGHT = 3
REJECT_WEIGHT = -2
LIKE_WEIGHT = 1
DISLIKE_WEIGHT = -1

NOT_FOUND_HISTORY = HTTPException(
  status_code=status.HTTP_400_BAD_REQUEST,
  detail='not found history',
)

def argsort(arr, reverse=False):
    """
    Return the indices that would sort the input array in ascending order.
    """
    return sorted(range(len(arr)), key=lambda i: arr[i],reverse=reverse)

def get_stat_score(user_id: str, exclude_clusters: List[int] = []):
  return userStatDb.find({ 'userId': ObjectId(user_id), 'clusterId': exclude_clusters})

def calculate_score(user_id: str,force: bool = False):
  exclude_clusters = find_last_week_accept_cluster(user_id)

  card_score = get_stat_score(user_id,exclude_clusters)
  month_predict_score = find_month_cluster(user_id,exclude_clusters)

  if not force and not month_predict_score and not exclude_clusters:
    raise NOT_FOUND_HISTORY

  cluster_score = [0] * 48

  for exclude_cluster in exclude_clusters:
    cluster_score[exclude_cluster] = -float('inf')

  for card in card_score:
    score = card['like'] * LIKE_WEIGHT + card['dislike'] * DISLIKE_WEIGHT
    cluster_score[card['clusterId']] += score 
  
  for month_predict in month_predict_score:
    score = month_predict['accept'] * ACCEPT_WEIGHT + month_predict['reject'] * REJECT_WEIGHT
    cluster_score[month_predict['_id']] += score 

  # [3, 1, 5 ...., 2]
  return argsort(cluster_score,reverse=True)
  
async def prediction_food(user_id: str,force: bool):
  ban_id_list = get_all_ban_food_id(user_id)
  cluster_scores = calculate_score(user_id,force)

  food = foodDb.aggregate([
    {'$match': { '_id': { '$nin': ban_id_list}}},
    { "$addFields" : { "__order" : { "$indexOfArray" : [ cluster_scores, "$clusterId" ] } } },
    { "$sort" : { "__order" : 1 } },
    { '$limit': 30 },
    {'$sample': {'size': 5}}
  ])
  
  return ListFoodResponse(data=list(food))

async def submit_prediction_result(userId: str,foodId: str, impress: bool,predict:bool = True):
  food_freq = create_or_find_food_frequency_db(userId,foodId)
  add_frequency(food_freq.id,success=impress)
  add_log_food_history(userId,foodId,is_success=impress,predict=predict)

  return {
    "result": "add frequency and log successfully"
  }
