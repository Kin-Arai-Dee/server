from code import interact
from pydantic import Field
from models.utils import MongoBaseModel, PyObjectId

class FoodFrequency(MongoBaseModel):
	id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
	frequency: int = Field(default=0)
	successCount: int = Field(default=0)
	successRandomCount: int = Field(default=0)
	failCount: int = Field(default=0)
	isFavorite: bool = Field(default=False)
	isBan: bool = Field(default=False)
	isNeverShow: bool = Field(default=False)
	foodId: PyObjectId = Field(...)
	userId: PyObjectId = Field(...)
	interact: int = Field(default=0)
