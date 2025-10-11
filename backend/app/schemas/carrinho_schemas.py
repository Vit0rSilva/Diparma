# app/schemas/carrinho_schemas.py
from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from app.schemas.item_schemas import ItemResponse

class CarrinhoResponse(BaseModel):
    id: str  # UUID string
    item: ItemResponse
    criado_em: datetime
    atualizado_em: datetime

    model_config = {"from_attributes": True}

class CarrinhoListResponse(BaseModel):
    itens: List[CarrinhoResponse]
    total_itens: int
