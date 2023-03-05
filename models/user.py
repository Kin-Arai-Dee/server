from datetime import datetime
from typing import List, NewType, Optional
from pydantic import BaseModel, EmailStr, Field
from .utils import MongoBaseModel, PyObjectId

class Token(BaseModel):
	accessToken: str
	tokenType: str

class TokenData(BaseModel):
	id: str
	username: str

class BaseUser(MongoBaseModel):
	username: str = Field(...)
	email: EmailStr = Field(...)
	withDescription: bool = Field(default=False)
	gender: Optional[str] = Field(default=None)
	age: Optional[int] = Field(default=None)
	weight: Optional[float] = Field(default=None)
	height: Optional[float] = Field(default=None)
	banFood: Optional[List[PyObjectId]] = Field(default_factory=list)

class User(BaseUser):
	id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

class UserInDB(User):
    hashed_password: str
