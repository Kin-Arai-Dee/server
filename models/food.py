from typing import List, Optional
from pydantic import BaseModel, Field
from models.utils import MongoBaseModel, PyObjectId

class BaseIngredient(BaseModel):
	ingredientName: str = Field(...)
	amount: float = Field(...)
	unit: str = Field(...)

class Ingredient(BaseModel):
	id: PyObjectId = Field(default_factory=PyObjectId,alias="_id")
	ingredientName: str = Field(...)

class BaseTag(BaseModel):
	externalId: str = Field(...)
	primaryName: str = Field(...)

class Tag(BaseTag):
	id: PyObjectId = Field(default_factory=PyObjectId,alias="_id")

class BaseFood(MongoBaseModel):
	title: str = Field(...)
	url: str = Field(...)
	imageUrl: str = Field(...)
	allTimeScore: int = Field(default=0)
	view: int = Field(default=0)
	totalLike: int = Field(default=0)
	ingredients: List[BaseIngredient] = Field(default_factory=list)
	ingredientTags: List[BaseTag] = Field(default_factory=list)
	categories: List[BaseTag] = Field(default_factory=list)
	methods: List[BaseTag] = Field(default_factory=list)
	isHealthy: bool = Field(default=False)
	calories: int = Field(default=0)
	isSpicy: int = Field(default=0)
	clusterId: int = Field(default=0)
	
class Food(BaseFood):
	id: PyObjectId = Field(default_factory=PyObjectId,alias="_id")
	tagIds: List[PyObjectId] = Field(default_factory=list)
	ingredientIds: List[PyObjectId] = Field(default_factory=list)
