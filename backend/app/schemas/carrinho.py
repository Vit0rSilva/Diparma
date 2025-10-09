from pydantic import BaseModel, conint, constr
from typing import Optional
from uuid import UUID

class CarrinhoBase(BaseModel):
    item_id: int
    usuario_id: UUID
    subtotal: conint(ge=0)

    model_config = {"from_attributes": True}