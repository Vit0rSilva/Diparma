from pydantic import BaseModel, conint, constr, confloat
from typing import Optional
from uuid import UUID

class BebidaBase(BaseModel):
    nome: constr(min_length=1, max_length=100)
    preco: confloat(ge=0)
    precoDesconto: Optional[confloat(ge=0)] = None
    desconto: Optional[bool] = False
    descricao: constr(min_length=1, max_length=255)
    imagem_url: constr(min_length=1, max_length=255)
    estrela: Optional[conint(ge=0, le=5)] = None
    legenda: constr(min_length=1, max_length=100)
    unidadeMedida: conint(ge=0)
    tipo_bebida_id: int

    class Config:
        orm_mode = True






 