from pydantic import BaseModel,Optional, EmailStr,conint , constr, validator
from uuid import UUID 
from typing import Optional

class ItemBase(BaseModel):
    prato_id =  UUID = None 
    bebida_id = UUID = None 
    extra_id = UUID = None 
    quantidade_prato = conint(ge=0, le=100)
    quantidade_extra = conint(ge=0, le=100) = None

    model_config = {"from_attributes": True}