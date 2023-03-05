from pydantic import Field
from models.utils import MongoBaseModel, PyObjectId


class FoodHistory(MongoBaseModel):
	id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
	foodId: PyObjectId = Field(default_factory=PyObjectId)
	userId: PyObjectId = Field(default_factory=PyObjectId)
	isSuccess: bool = Field(...)
	clusterId: int = Field(...)
	isRandom: bool = Field(default=True)
