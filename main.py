from datetime import timedelta
from fastapi import Depends, FastAPI, HTTPException, status
from models.user import NewUser, User
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware

from models.user import Token
from config.db import userDb
from routes.pm import pm
from routes.light import light
from schemas.user import authenticate_user, create_access_token, get_current_active_user, get_password_hash

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

app = FastAPI(
    title="LigthingHoleApp"
)

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pm,tags=['pm'])
app.include_router(light,tags=['light'])

@app.get("/",tags=['check'])
async def check_app():
    return {"message": "API is running."}

@app.post("/login",tags=['user'])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    userData = dict(user)
    del userData['hashed_password']
    return {"accessToken": access_token, "tokenType": "bearer", 'user': userData}

@app.get("/users/me/", response_model=User,tags=['user'])
async def read_users_data(current_user: User = Depends(get_current_active_user)):
    return current_user

@app.post('/register',tags=['user'])
async def register_new_user(user: NewUser):
    account = userDb.find_one({'username': user.username})
    if account:
        raise HTTPException(status_code='400',detail='username must be unique. Already have this account.')
    hash_pasword = get_password_hash(user.password)
    userData = dict(user)
    del userData['password']
    _id = userDb.insert_one({
        **userData,
        'hashed_password': hash_pasword,
        'disabled': False,
        'permission': 0,
    }).inserted_id
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {
        'message': 'register success',
        'accessToken': access_token,
        'data': {
            **userData,
            'userId': str(_id)
        }
    }
