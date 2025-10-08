from pydantic import BaseModel, conint, constr
from typing import Optional
from uuid import UUID

class EnderecoBase(BaseModel):
    rua: constr(min_length=1, max_length=255)
    numero: constr(min_length=1, max_length=20)
    complemento: Optional[constr(max_length=100)] = None
    bairro: constr(min_length=1, max_length=100)
    cidade: constr(min_length=1, max_length=100)
    cep: constr(min_length=8, max_length=8)
    complemento: constr(max_length=100) = None
    lat: constr(max_length=50) = None
    lng: constr(max_length=50) = None
    usuario_id: UUID

    class Config:
        orm_mode = True