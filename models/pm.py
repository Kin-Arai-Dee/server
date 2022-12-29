from datetime import datetime
from typing import Optional
from pydantic import BaseModel

# class PostPmStatus(BaseModel):
#     pm1: float
#     pm10: float
#     pm25: float
#     Timestamp: Optional[datetime]

class PmStatus(BaseModel):
    # poleId: str
    pm1: float
    pm10: float
    pm25: float
    # Timestamp: float
