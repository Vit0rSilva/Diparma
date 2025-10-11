from pydantic import BaseModel, conint, constr, confloat
from typing import Optional
from uuid import UUID
from app.schemas.tipoPrato_schemas import TipoPratoResponse

class PratoBase(BaseModel):
    desconto: Optional[conint(ge=0, le=1)] = 0
    precoDesconto: Optional[confloat(ge=0)] = None
    kcal: Optional[conint(ge=0)] = None
    estrela: Optional[conint(ge=0, le=5)] = None
    legenda: Optional[constr(max_length=100)] = None

    model_config = {"from_attributes": True}

class PratoCreate(PratoBase):
    nome: constr(min_length=1, max_length=100)
    preco: confloat(ge=0)
    pessoas: conint(ge=1)
    peso: conint(ge=1)
    descricao: constr(min_length=1, max_length=255)
    imagem_url: constr(min_length=1, max_length=255)
    tipo_prato_id: int

class PratoUpdate(PratoBase):
    nome: Optional[constr(min_length=1, max_length=100)] = None
    preco: Optional[confloat(ge=0)] = None
    pessoas: Optional[conint(ge=1)] = None
    peso: Optional[conint(ge=1)] = None
    descricao: Optional[constr(min_length=1, max_length=255)] = None
    imagem_url: Optional[constr(min_length=1, max_length=255)] = None
    tipo_prato_id: Optional[int] = None

class PratoResponse(PratoBase):
    id: UUID
    nome: Optional[constr(min_length=1, max_length=100)] = None
    preco: Optional[confloat(ge=0)] = None
    pessoas: Optional[conint(ge=1)] = None
    peso: Optional[conint(ge=1)] = None
    descricao: Optional[constr(min_length=1, max_length=255)] = None
    imagem_url: Optional[constr(min_length=1, max_length=255)] = None
    tipo_prato_id: Optional[int] = None
    tipo_prato: Optional[TipoPratoResponse] = None
