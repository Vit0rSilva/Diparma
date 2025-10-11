from pydantic import BaseModel
from uuid import UUID 

class TipoPratoBase(BaseModel):
    tipo: str

    model_config = {"from_attributes": True}

class TipoPratoCreate(TipoPratoBase):
    pass

class TipoPratoUpdate(TipoPratoBase):
    pass

class TipoPratoResponse(TipoPratoBase):
    id: int