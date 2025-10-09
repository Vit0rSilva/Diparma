from pydantic import BaseModel,Optional, EmailStr,conint , constr, validator
from uuid import UUID 

class TipoPratoBase(BaseModel):
    tipo: str

    model_config = {"from_attributes": True}