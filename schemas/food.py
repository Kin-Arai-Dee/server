from typing import List

from pydantic import BaseModel, Field, root_validator
from models.utils import PyObjectId
from models.food import BaseFood, Ingredient, Tag
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

class FoodNameResponse(BaseModel):
	data: List[FoodResponse]

	class Config:
		allow_population_by_field_name = True
		arbitrary_types_allowed = True
		json_encoders={
        ObjectId: str,
    }

class TopIngredientResponse(BaseModel):
	id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
	count: int
	ingredientName: str

	class Config:
			allow_population_by_field_name = True
			arbitrary_types_allowed = True
			json_encoders = {ObjectId: str}

class TopIngredientListResponse(BaseModel):
	other: List[TopIngredientResponse] = Field(default_factory=list)
	protein: List[TopIngredientResponse] = Field(default_factory=list)
	carbo: List[TopIngredientResponse] = Field(default_factory=list)
	mineral: List[TopIngredientResponse] = Field(default_factory=list)
	vitamit: List[TopIngredientResponse] = Field(default_factory=list)
	class Config:
		allow_population_by_field_name = True
		arbitrary_types_allowed = True
		json_encoders={
        ObjectId: str,
    }

class IngredientListResponse(BaseModel):
	data: List[Ingredient] = Field(default_factory=list)
	
	class Config:
		allow_population_by_field_name = True
		arbitrary_types_allowed = True
		json_encoders={
        ObjectId: str,
    }
class TagListResponse(BaseModel):
	data: List[Tag] = Field(default_factory=list)
	class Config:
		allow_population_by_field_name = True
		arbitrary_types_allowed = True
		json_encoders={
				ObjectId: str,
	}