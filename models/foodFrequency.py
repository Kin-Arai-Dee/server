from code import interact
from datetime import datetime
from pydantic import BaseModel, Field
from models.utils import MongoBaseModel, PyObjectId

class FoodFrequency(MongoBaseModel):
	id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
	successCount: int = Field(default=0)
	failCount: int = Field(default=0)
	isBan: bool = Field(default=False)
	foodId: PyObjectId = Field(...)
	userId: PyObjectId = Field(...)
	interact: int = Field(default=0)

class FoodFrequencyDefault(BaseModel):
	successCount: int = Field(default=0)
	failCount: int = Field(default=0)
	interact: int = Field(default=0)
	createAt: datetime = Field(default_factory=datetime.now)