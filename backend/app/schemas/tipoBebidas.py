from pydantic import BaseModel, EmailStr,conint , constr, validator

class TipoBebidaBase(BaseModel):
    tipo: str

    model_config = {"from_attributes": True}