from typing import List
from config.db import userDb
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer 
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from models.user import UserInDB 
from schemas.user import AuthResponse, RegisterRequest, RenewToken, TokenResponse, UpdateUserDescription, UpdateUserRequest, UserResponse
from services.authorize import create_access_token, create_refresh_token, verify_access_token, verify_refresh_token
from services.food import get_food_id_by_ingredient
from services.foodFrequency import ban_food_by_id
from services.utils import verify_password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

USER_NOT_FOUND_ERROR = HTTPException(
		status_code=status.HTTP_400_BAD_REQUEST,
		detail="User not found",
)

def get_user(user_id: str):
	result = userDb.find_one({ '_id': ObjectId(user_id) })
	if result:
			return UserInDB(**result)

def get_user_from_user_name(username: str):
	result = userDb.find_one({'username': username })
	if result:
			return UserInDB(**result)

def authenticate_user(username: str, password: str):
	user = get_user_from_user_name(username)
	if not user:
			return False
	if not verify_password(password, user.hashed_password):
			return False
	return user

async def verify_user(request: Request,token: str = Depends(oauth2_scheme)):
	token_data = await verify_access_token(token)
	request.state.user = token_data
	return token_data

async def get_current_user(request: Request,token: str = Depends(oauth2_scheme)):
	token_data = await verify_access_token(token)
	user = get_user(token_data.id)
	if user is None:
			raise USER_NOT_FOUND_ERROR
	request.state.user = user
	return user

async def checkUser(request: Request,user_id:str):
	if str(request.state.user.id) != user_id:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='invalid user id')
	return user_id

async def get_token_response(user):
	access_token, expire_token = create_access_token(
		data={"sub": str(user["id"]), "name": user["username"]}
	)
	refresh_token, expire_refresh_token = create_refresh_token(
		data={"sub": str(user["id"]), "name": user["username"]}
	)

	return TokenResponse(
		accessToken=access_token,tokenExpire=expire_token,refreshToken=refresh_token,refreshTokenExpire=expire_refresh_token
	)


async def refresh_token(renew_token: RenewToken): 
	token_data = await verify_refresh_token(renew_token.refreshToken)
	await verify_access_token(renew_token.accessToken, True)

	return get_token_response(token_data)


async def register_user(user: RegisterRequest):
	userData = UserInDB(**jsonable_encoder(user))

	userDb.insert_one(userData.dict(by_alias=True))

	tokenResponse = await get_token_response(userData.dict())

	return AuthResponse(user=userData, **jsonable_encoder(tokenResponse))

async def accessToken_for_login(user: UserInDB):
	tokenResponse = await get_token_response(user.dict())

	return AuthResponse(user=user, **jsonable_encoder(tokenResponse))

def ban_food_by_ingredient(user_id:str,  ingredients: List[str]):
	food_id_list = get_food_id_by_ingredient(ingredients)
	ban_food_by_id(user_id,food_id_list)

async def update_user_description(user_id: str,updateData: UpdateUserRequest) -> UpdateUserDescription:
	updateDescritpion = UpdateUserDescription(**updateData.dict())

	userDb.update_one({'_id': ObjectId(user_id)},{
		'$set': updateDescritpion.dict()
	})

	if updateDescritpion.banFood:
		ban_food_by_ingredient(user_id,updateDescritpion.banFood)

	return updateDescritpion

async def update_ready_user(user_id: str) -> UserResponse:
	userDb.update_one({'_id' : ObjectId(user_id)}, {
		'$set': {
			'withDescription': True
		}
	})

	user = userDb.find_one({'_id' : ObjectId(user_id)})

	return UserResponse(**user)
