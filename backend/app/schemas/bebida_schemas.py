from pydantic import BaseModel, conint, constr, confloat
from typing import Optional
from uuid import UUID
from app.schemas.tipoBebidas_schemas import TipoBebidaResponse

class BebidaBase(BaseModel):
    precoDesconto: Optional[confloat(ge=0)] = None
    desconto: Optional[bool] = False
    estrela: Optional[confloat(ge=0, le=5)] = None

    model_config = {"from_attributes": True}

class BebidaCreate(BebidaBase):
    nome: constr(min_length=1, max_length=100)
    preco: confloat(ge=0)
    descricao: constr(min_length=1, max_length=255)
    imagem_url: constr(min_length=1, max_length=255)
    legenda: constr(min_length=1, max_length=100)
    unidadeMedida: conint(ge=0)
    tipo_bebida_id: int

class BebidaUpdate(BebidaBase):
    nome: Optional[constr(min_length=1, max_length=100)] = None
    preco: Optional[confloat(ge=0)] = None
    descricao: Optional[constr(min_length=1, max_length=255)] = None
    imagem_url: Optional[constr(min_length=1, max_length=255)] = None
    tipo_bebida_id: Optional[int] = None
    legenda: Optional[constr(min_length=1, max_length=100)] = None
    unidadeMedida: Optional[conint(ge=0)] = None

class BebidaResponse(BebidaBase):
    id: UUID
    nome: Optional[constr(min_length=1, max_length=100)] = None
    preco: Optional[confloat(ge=0)] = None
    descricao: Optional[constr(min_length=1, max_length=255)] = None
    imagem_url: Optional[constr(min_length=1, max_length=255)] = None
    tipo_bebida_id: Optional[int] = None
    tipo_bebida: Optional[TipoBebidaResponse] = None
    legenda: Optional[constr(min_length=1, max_length=100)] = None
    unidadeMedida: Optional[conint(ge=0)] = None
