from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field
from datetime import datetime, timezone

class PyObjectId(ObjectId):
  @classmethod
  def __get_validators__(cls):
      yield cls.validate

  @classmethod
  def validate(cls, v):
      if not ObjectId.is_valid(v):
          raise ValueError("Invalid objectid")
      return ObjectId(v)

  @classmethod
  def __modify_schema__(cls, field_schema):
      field_schema.update(type="string")

class MongoBaseModel(BaseModel):
	createAt: Optional[datetime] = Field(default_factory=datetime.now)
	updateAt: Optional[datetime] = Field(default_factory=datetime.now)
	
	class Config:
		allow_population_by_field_name = True
		arbitrary_types_allowed = True
		json_encoders={
        ObjectId: str,
        datetime: lambda dt: dt.replace(tzinfo=timezone.utc)
              .isoformat()
              .replace("+00:00", "Z")
      }

class PaginateModel(BaseModel):
  start: int = Field(default=0)
  limit: int = Field(default=10)
  hasNext: bool = Field(default=False)
