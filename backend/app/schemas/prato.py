from pydantic import BaseModel, conint, constr
from typing import Optional

class PratoBase(BaseModel):
    nome: constr(min_length=1, max_length=100)
    preco: conint(ge=0)
    precoDesconto: conint(ge=0) = None  # define default None
    desconto: conint(ge=0) = 0
    pessoas: conint(ge=1)
    kcal: conint(ge=0) = None
    peso: conint(ge=1)
    descricao: constr(min_length=1, max_length=255)
    imagem_url: constr(min_length=1, max_length=255)
    estrela: conint(ge=0, le=5) = None
    legenda: constr(max_length=100) = None
    tipo: constr(max_length=50) = None
    tipo_prato_id: int

    model_config = {"from_attributes": True}
