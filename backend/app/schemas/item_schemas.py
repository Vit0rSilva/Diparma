# app/schemas/item_schemas.py
from pydantic import BaseModel, conint
from typing import Optional
from uuid import UUID
from datetime import datetime

class ItemBase(BaseModel):
    prato_id: Optional[UUID] = None
    bebida_id: Optional[UUID] = None
    extra_id: Optional[UUID] = None
    quantidade_prato: conint(ge=1) = 1
    quantidade_extra: conint(ge=0) = 0

    model_config = {"from_attributes": True}

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    quantidade_prato: Optional[conint(ge=1)] = None
    quantidade_extra: Optional[conint(ge=0)] = None

class NestedProduto(BaseModel):
    id: UUID
    nome: Optional[str] = None
    preco: Optional[float] = None
    imagem_url: Optional[str] = None

    model_config = {"from_attributes": True}

class ItemResponse(ItemBase):
    id: int
    prato: Optional[NestedProduto] = None
    bebida: Optional[NestedProduto] = None
    extra: Optional[NestedProduto] = None
    criado_em: Optional[datetime] = None
    atualizado_em: Optional[datetime] = None
