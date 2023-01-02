from datetime import datetime, timezone
from typing import List, NewType, Optional
from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field, root_validator

from models.user import BaseUser, Gender
from models.utils import PyObjectId
from services.utils import get_password_hash

class RenewToken(BaseModel):
	accessToken: str = Field(...)
	refreshToken: str = Field(...)

class TokenResponse(RenewToken):
	tokenType: str = Field(default='Bearer')
	tokenExpire: datetime = Field(...)
	refreshTokenExpire: datetime = Field(...)

	class Config:
		allow_population_by_field_name = True
		arbitrary_types_allowed = True
		json_encoders={
      datetime: lambda dt: dt.replace(tzinfo=timezone.utc)
        .isoformat()
        .replace("+00:00", "Z")
    }

class UserResponse(BaseUser):
	userId: PyObjectId
	withDescription: bool

	@root_validator(pre=True)
	def remove_id(cls,values):
		if('id' in values):
			values["userId"] = values.pop('id')
		elif('_id' in values):
			values["userId"] = values.pop('_id')
		values["withDescription"] = bool(values["gender"])

		return values

class RegisterRequest(BaseModel):
	username: str = Field(...)
	email: EmailStr = Field(...)
	hashed_password: str = Field(...)

	@root_validator(pre=True)
	def hash_password(cls,values):
		if('password' in values):
			values["hashed_password"] =  get_password_hash(values.pop('password'))
		return values

class AuthResponse(TokenResponse):
	user: UserResponse = Field(...)
	class Config:
		allow_population_by_field_name = True
		arbitrary_types_allowed = True
		json_encoders={
        ObjectId: str,
        datetime: lambda dt: dt.replace(tzinfo=timezone.utc)
              .isoformat()
              .replace("+00:00", "Z")
      }

class UpdateUserDescription(BaseModel):
	gender: str
	age: int = Field(default_factory=None)
	weight: float = Field(...)
	height: float = Field(...)
	banfood: List[str] = Field(default_factory=list)

class UpdateUserRequest(UpdateUserDescription):
	lastMenu: List[str]
	isFirstTime: bool = Field(default=False)
