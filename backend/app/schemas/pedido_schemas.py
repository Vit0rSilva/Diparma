from pydantic import BaseModel, constr
from typing import List, Optional
from uuid import UUID
from datetime import datetime

class PedidoItemCreate(BaseModel):
    nome: str
    quantidade: int
    preco_unitario: float
    subtotal: float

class PedidoCreate(BaseModel):
    carrinho_id: str
    frete: Optional[float] = None
    retirada_boll: Optional[bool] = False
    horario_retirada: Optional[str] = None
    observacao: Optional[str] = None

class PedidoItemResponse(BaseModel):
    id: int
    nome: str
    quantidade: int
    preco_unitario: float
    subtotal: float

class PedidoResponse(BaseModel):
    id: str
    usuario_id: str
    status: str
    total: float
    id_endereco: Optional[str] = None
    frete: Optional[float] = None
    retirada_boll: Optional[bool] = False
    horario_retirada: Optional[str] = None
    observacao: Optional[str] = None
    itens: List[PedidoItemResponse]
    criado_em: datetime
    atualizado_em: datetime

    model_config = {"from_attributes": True}

