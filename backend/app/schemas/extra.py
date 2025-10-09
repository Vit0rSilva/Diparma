from pydantic import BaseModel, conint, constr
from typing import Optional

class ExtraBase(BaseModel):
    nome: constr(min_length=1, max_length=100)
    preco: conint(ge=0)
    descricao: constr(min_length=1, max_length=255)
    kcal: conint(ge=0) = None
    peso: conint(ge=1)
    imagem_url: constr(min_length=1, max_length=255)
    estrela: conint(ge=0, le=5) = None
    legenda: constr(max_length=100)

    model_config = {"from_attributes": True}