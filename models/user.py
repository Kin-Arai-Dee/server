from typing import List, NewType, Optional
from pydantic import BaseModel, EmailStr, Field
from .utils import MongoBaseModel, PyObjectId
from enum import Enum
class Gender(Enum):
	MALE = 'male'
	FEMALE = 'female'

class Token(BaseModel):
	accessToken: str
	tokenType: str

class TokenData(BaseModel):
	id: str
	username: str

class BaseUser(MongoBaseModel):
	username: str = Field(...)
	email: EmailStr = Field(...)
	gender: Optional[NewType('Gender', Gender)] = Field(...)
	age: Optional[int] = Field(...)
	weight: Optional[float] = Field(...)
	height: Optional[float] = Field(...)
	banFood: Optional[List[str]] = Field(default_factory=list)

class User(BaseUser):
	id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

class UserInDB(User):
    hashed_password: str
