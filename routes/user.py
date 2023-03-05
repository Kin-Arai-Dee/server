from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from models.user import UserInDB
from schemas.history import FoodHistoryResponse
from schemas.user import AuthResponse, RegisterRequest, RenewToken, TokenResponse, UpdateUserRequest, UserResponse
from services.foodHistory import find_log_food_history
from services.user import (
  authenticate_user,
  checkUser,
  find_ban_ingredients_name, 
  get_current_user, 
  accessToken_for_login,
  get_user_from_user_name,
	refresh_token,
  register_user,
  update_ready_user,
  update_user_description,
  verify_user,
)

user = APIRouter()

@user.post("/login",response_model=AuthResponse)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
	user = authenticate_user(form_data.username, form_data.password)
	if not user:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Incorrect username or password",
			headers={"WWW-Authenticate": "Bearer"},
		)
	return await accessToken_for_login(user)

@user.get("/user/me", response_model=UserResponse)
async def read_users_data(current_user: UserInDB = Depends(get_current_user)):
  return current_user

@user.post('/register', response_model=AuthResponse)
async def register_new_user(user: RegisterRequest):
	account = get_user_from_user_name(user.username)
	if account:
		raise HTTPException(status_code=400,detail='username must be unique. Already have this account.')

	return await register_user(user)

@user.post('/refresh', response_model=TokenResponse)
async def renew_access_token(renew_token: RenewToken):
	return await refresh_token(renew_token)


@user.patch('/user/{user_id}',response_model=UserResponse)
async def update_user(updateUserData: UpdateUserRequest,user=Depends(get_current_user),user_id=Depends(checkUser)):
	updated_data = await update_user_description(user_id,updateUserData)

	merge_user = {**user.dict(),**updated_data.dict()}

	banFood = find_ban_ingredients_name(merge_user.pop('banFood'))

	return UserResponse(**merge_user,banFood=banFood)


@user.get('/user/history/{user_id}', response_model=FoodHistoryResponse)
async def get_user_prediction_food_history(start: int = 0,limit: int =30,_=Depends(verify_user),user_id=Depends(checkUser)):
	return find_log_food_history(user_id,start,limit)

@user.patch('/user/ready/{user_id}',response_model=UserResponse)
async def set_user_to_ready_to_use(_=Depends(verify_user),user_id=Depends(checkUser)):
	return await update_ready_user(user_id)
