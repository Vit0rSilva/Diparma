from pydantic import BaseModel, constr, condecimal, conint
from typing import Optional
from uuid import UUID

class ExtraBase(BaseModel):
    preco: condecimal(max_digits=10, decimal_places=2)
    descricao: constr(min_length=1, max_length=255)
    kcal: Optional[condecimal(max_digits=10, decimal_places=1)] = None
    peso: condecimal(max_digits=10, decimal_places=1)
    imagem_url: constr(min_length=1, max_length=255)
    estrela: Optional[conint(ge=0, le=5)] = None
    legenda: constr(min_length=1, max_length=100)

    model_config = {"from_attributes": True}

class ExtraCreate(ExtraBase):
    nome: constr(min_length=1, max_length=100)

class ExtraUpdate(BaseModel):
    nome: Optional[constr(min_length=1, max_length=100)] = None
    preco: Optional[condecimal(max_digits=10, decimal_places=2)] = None
    descricao: Optional[constr(min_length=1, max_length=255)] = None
    kcal: Optional[condecimal(max_digits=10, decimal_places=1)] = None
    peso: Optional[condecimal(max_digits=10, decimal_places=1)] = None
    imagem_url: Optional[constr(min_length=1, max_length=255)] = None
    estrela: Optional[conint(ge=0, le=5)] = None
    legenda: Optional[constr(min_length=1, max_length=100)] = None

class ExtraResponse(ExtraBase):
    id: UUID
    nome: constr(min_length=1, max_length=100)
