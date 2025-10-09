from datetime import time
from pydantic import BaseModel, conint, constr
from typing import Optional

class PedidoBase(BaseModel):
    item_id: int
    usuario_id: constr(min_length=1, max_length=36)
    endereco_id: int
    frete = conint(ge=0) = None
    retirada_loja = conint(ge=0) = 0 
    retirada_hora: time = None
    total: conint(ge=0)
    status: constr(min_length=1, max_length=50) = "Pendente"  # Default status
    observacoes: Optional[constr(max_length=255)] = None

    model_config = {"from_attributes": True}