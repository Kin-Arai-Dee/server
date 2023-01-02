from pydantic import BaseModel


class PredictionSubmitRequest(BaseModel):
  impress: bool

