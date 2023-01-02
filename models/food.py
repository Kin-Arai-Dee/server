from typing import Optional
from pydantic import Field
from models.utils import MongoBaseModel, PyObjectId


class BaseFood(MongoBaseModel):
	foodName: str = Field(...)
	imageUrl: str = Field(...)
	ingredient1: str = Field(...)
	ingredient2: Optional[str] = Field(...)
	predictionPrice: int = Field(...)
	calories: int = Field(...)
	categorie: str = Field(...)
	cookMethod: str = Field(...)
	isSpicy: bool = Field(...)

class Food(BaseFood):
	id: PyObjectId = Field(default_factory=PyObjectId,alias="_id")
