from pymongo import MongoClient
from decouple import config

client = MongoClient(config('MONGO_URL'))

userDb = client.KinAriDee.User
foodDb = client.KinAriDee.Food
foodFreqDb = client.KinAriDee.FoodFrequency
foodHistoryDb = client.KinAriDee.FoodHistory
