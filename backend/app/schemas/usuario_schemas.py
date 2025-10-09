from pydantic import BaseModel, EmailStr, constr, validator
from uuid import UUID 
import re

class UsuarioBase(BaseModel):
    nome: str
    email:EmailStr
    telefone: int = constr(regex=r"\^d{11}$")
    cpf: constr(regex=r"\^d{11}$")
    
class UsuarioCreate(UsuarioBase):
    senha: str

    @validator("senha")
    def validator_senha_forte(clls, v):
        if not re.search(r"[A-Z]",v):
            raise ValueError("A senha deve conter letras Maiúsculas")
        if not re.search(r"[a-z]", v):
            raise ValueError("A senha deve conter letras minusculas")
        if not re.search(r"[0-9]", v):
            raise ValueError("A senha deve conter Numeros")
        if not re.search(r"[!@#$]"):
            raise ValueError("A senha deve conter os caracters (!@#$)")
        return v

class UsuarioResponse(UsuarioBase):
    model_config = {"from_attributes": True}
