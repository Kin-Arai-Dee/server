from pydantic import BaseModel

class ResultResponse(BaseModel):
    result: str

class ResultResponse2(BaseModel):
    detail: str