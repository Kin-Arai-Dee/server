from pymongo import MongoClient
from decouple import config

client = MongoClient(config('MONGO_URL2'))

userDb = client.KinAriDee.User
foodDb = client.KinAriDee.Food
foodFreqDb = client.KinAriDee.FoodFrequency
foodHistoryDb = client.KinAriDee.FoodHistory
methodDb = client.KinAriDee.Method
tagDb = client.KinAriDee.Tag
categoryDb = client.KinAriDee.Category
ingredientDb = client.KinAriDee.ingredient
userStatDb = client.KinAriDee.UserStat