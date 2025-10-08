from pydantic import BaseModel,Optional, EmailStr,conint , constr, validator
from uuid import UUID 

class TipoPratoBase(BaseModel):
    tipo: str

    class Config:
        orm_mode = True