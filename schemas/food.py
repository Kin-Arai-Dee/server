from typing import List

from pydantic import BaseModel, Field, root_validator
from models.utils import PyObjectId
from models.food import BaseFood
from bson import ObjectId

class FoodIdResponse(BaseModel):
	foodId: PyObjectId

	@root_validator(pre=True)
	def remove_id(cls,values):
		if('id' in values):
			values["foodId"] = values.pop('id')
		elif('_id' in values):
			values["foodId"] = values.pop('_id')

		return values

class FoodResponse(BaseFood, FoodIdResponse):
	pass

class FoodName(FoodIdResponse):
	foodName: str = Field(...)
	imageUrl: str = Field(...)
	calories: int = Field(...)
	categorie: str = Field(...)
	cookMethod: str = Field(...)
	interact: int = Field(...)

class FoodNameResponse(BaseModel):
	data: List[FoodName]

	class Config:
		allow_population_by_field_name = True
		arbitrary_types_allowed = True
		json_encoders={
        ObjectId: str,
    }
