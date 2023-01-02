from fastapi import Depends, HTTPException, status, APIRouter, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder
from models.user import User
from schemas.user import AuthResponse, RegisterRequest, RenewToken, TokenResponse, UpdateUserRequest, UserResponse
from services.foodHistory import find_log_food_history
from services.user import (
  authenticate_user,
  checkUser, 
  get_current_active_user,
  get_current_user, 
  get_user,
  accessToken_for_login,
	refresh_token,
  register_user,
  update_user_description,
)

user = APIRouter()

@user.post("/login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
	user = authenticate_user(form_data.username, form_data.password)
	if not user:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Incorrect username or password",
			headers={"WWW-Authenticate": "Bearer"},
		)
	return await accessToken_for_login(user)

@user.get("/users/me/", response_model=User)
async def read_users_data(current_user: User = Depends(get_current_active_user)):
  return current_user

@user.post('/register', response_model=AuthResponse)
async def register_new_user(user: RegisterRequest):
	account = get_user(user.username)
	if account:
		raise HTTPException(status_code=400,detail='username must be unique. Already have this account.')

	return await register_user(user)

@user.post('/refresh', response_model=TokenResponse)
async def renew_access_token(renew_token: RenewToken):
	return await refresh_token(renew_token)


@user.patch('/user/{user_id}')
async def update_user(updateUserData: UpdateUserRequest,user=Depends(get_current_user),user_id=Depends(checkUser)):
	updated_data = await update_user_description(user_id,updateUserData,first_time=updateUserData)

	return UserResponse(**{**user.dict(),**updated_data.dict()})

@user.get('/user/history/{user_id}')
async def update_user(start: int = 0,limit=30,user=Depends(get_current_user),user_id=Depends(checkUser)):
	return find_log_food_history(user_id,start,limit)