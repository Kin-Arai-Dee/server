from pydantic import Field, root_validator

from models.foodHistory import FoodHistory
from models.utils import PaginateModel
from bson import ObjectId
from datetime import datetime, timezone

from schemas.food import FoodResponse

class FoodHistoryItemResponse(FoodHistory):
	food: FoodResponse = Field(...)

class FoodHistoryResponse(PaginateModel):
  data: list[FoodHistoryItemResponse] = Field(...)

  @root_validator(pre=True)
  def validate_has_next(cls,values):
    values['hasNext'] = len(values["data"]) == values["limit"]

    return values

  class Config:
    allow_population_by_field_name = True
    arbitrary_types_allowed = True
    json_encoders={
        ObjectId: str,
        datetime: lambda dt: dt.replace(tzinfo=timezone.utc)
              .isoformat()
              .replace("+00:00", "Z")
      }
