from typing import List
from models.food import Ingredient, Tag
from schemas.food import FoodResponse
from pydantic import BaseModel, Field
from bson import ObjectId

class PredictionSubmitRequest(BaseModel):
	impress: bool
	predict: bool


class ListFoodResponse(BaseModel):
	data: List[FoodResponse] = Field(default_factory=list)
	
	class Config:
		allow_population_by_field_name = True
		arbitrary_types_allowed = True
		json_encoders={
				ObjectId: str,
	}