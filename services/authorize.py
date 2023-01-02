from datetime import datetime, timedelta
from http.client import HTTPException
from typing import Optional
from jose import JWTError, jwt, ExpiredSignatureError
from fastapi import HTTPException, status
from decouple import config

from models.user import TokenData
from services.utils import verify_password

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 # 1 day
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days

JWT_SECRET_KEY = config('JWT_SECRET_KEY')
JWT_REFRESH_SECRET_KEY = config('JWT_REFRESH_SECRET_KEY')
ALGORITHM = "HS256"

credentials_exception = HTTPException(
	status_code=status.HTTP_401_UNAUTHORIZED,
	detail="Could not validate credentials",
	headers={"WWW-Authenticate": "Bearer"},
)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
	to_encode = data.copy()
	if expires_delta:
			expire = datetime.utcnow() + timedelta(minutes=expires_delta)
	else:
			expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
	to_encode.update({"exp": expire})
	encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
	return (encoded_jwt , expire)

def create_refresh_token(data: dict, expires_delta: int = REFRESH_TOKEN_EXPIRE_MINUTES) -> str:
	to_encode = data.copy()
	if expires_delta:
			expire = datetime.utcnow() + timedelta(minutes=expires_delta)
	else:
			expire = datetime.utcnow() +  timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
	
	to_encode.update({"exp": expire})
	encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, algorithm=ALGORITHM)
	return encoded_jwt, expire

async def verify_access_token(token: str, checkExpire: bool = False):
	try:
		payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
		id: str = payload.get("sub")
		username: str = payload.get("name")
		if id is None:
				raise credentials_exception
		return TokenData(username=username,id=id)
	except ExpiredSignatureError:
		if(checkExpire):
			return True
		raise credentials_exception
	except JWTError:
		raise credentials_exception

async def verify_refresh_token(token: str):
	try:
		payload = jwt.decode(token, JWT_REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
		id: str = payload.get("sub")
		username: str = payload.get("name")
		if id is None:
				raise credentials_exception
		return TokenData(id=id,username=username)
	except JWTError:
		raise credentials_exception
