from pydantic import BaseModel, conint
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from app.schemas.prato_schemas import PratoResponse
from app.schemas.bebida_schemas import BebidaResponse
from app.schemas.extra_schemas import ExtraResponse

class CarrinhoItemCreate(BaseModel):
    prato_id: Optional[UUID] = None
    bebida_id: Optional[UUID] = None
    extra_id: Optional[UUID] = None
    quantidade_prato: conint(ge=0) = 0
    quantidade_bebida: conint(ge=0) = 0
    quantidade_extra: conint(ge=0) = 0

class CarrinhoItemUpdate(BaseModel):
    quantidade_prato: Optional[conint(ge=0)]
    quantidade_bebida: Optional[conint(ge=0)]
    quantidade_extra: Optional[conint(ge=0)]

class CarrinhoItemResponse(BaseModel):
    id: int
    prato: Optional[PratoResponse] = None
    bebida: Optional[BebidaResponse] = None
    extra: Optional[ExtraResponse] = None
    quantidade_prato: int
    quantidade_bebida: int
    quantidade_extra: int
    preco_unitario: float
    subtotal: float
    criado_em: datetime
    atualizado_em: datetime

    model_config = {"from_attributes": True}

class CarrinhoResponse(BaseModel):
    id: str
    usuario_id: str
    status: str
    itens: List[CarrinhoItemResponse]
    criado_em: datetime
    atualizado_em: datetime

    model_config = {"from_attributes": True}
