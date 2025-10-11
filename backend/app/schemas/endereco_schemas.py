from pydantic import BaseModel, constr
from typing import Optional
from uuid import UUID
from app.schemas.usuario_schemas import UsuarioBase

class EnderecoBase(BaseModel):
    rua: constr(min_length=1, max_length=255)
    numero: constr(min_length=1, max_length=10)
    bairro: constr(min_length=1, max_length=100)
    cidade: constr(min_length=1, max_length=100)
    complemento: Optional[constr(max_length=100)] = None
    cep: constr(min_length=8, max_length=8)
    lat: Optional[str] = None
    lng: Optional[str] = None

    model_config = {"from_attributes": True}

class EnderecoCreate(EnderecoBase):
    pass

class EnderecoUpdate(BaseModel):
    rua: Optional[constr(min_length=1, max_length=255)] = None
    numero: Optional[constr(min_length=1, max_length=10)] = None
    bairro: Optional[constr(min_length=1, max_length=100)] = None
    cidade: Optional[constr(min_length=1, max_length=100)] = None
    complemento: Optional[constr(max_length=100)] = None
    cep: Optional[constr(min_length=8, max_length=8)] = None
    lat: Optional[str] = None
    lng: Optional[str] = None

class EnderecoResponse(EnderecoBase):
    id: int
    usuario_id: UUID
    usuario: Optional[UsuarioBase] = None

