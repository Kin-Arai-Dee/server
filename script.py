from pydantic import BaseModel, root_validator


class TokenModel(BaseModel):
  token: str 
  hashed_password: str

  @root_validator(pre=True)
  def hash(cls,values):
    print(values)
    return values

a = {
  'password': '12',
  'token': '124' ,
  'hashed_password': '124'
}
TokenModel(**a)