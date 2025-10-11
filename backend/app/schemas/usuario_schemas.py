# app/schemas/usuario_schemas.py
from pydantic import BaseModel, EmailStr, constr, field_validator
from typing import Optional
from datetime import datetime
import re

class UsuarioBase(BaseModel):
    nome: constr(min_length=2, max_length=100)
    cpf: constr(min_length=11, max_length=11, pattern=r"^\d{11}$")
    email: EmailStr
    telefone: Optional[constr(min_length=8, max_length=20)] = None

    model_config = {"from_attributes": True}

class UsuarioCreate(UsuarioBase):
    senha: constr(min_length=8, max_length=128)

    @field_validator("senha")
    @classmethod
    def senha_regras(cls, v: str) -> str:
        if not re.search(r"[A-Z]", v):
            raise ValueError("A senha deve conter pelo menos uma letra maiúscula")
        if not re.search(r"[a-z]", v):
            raise ValueError("A senha deve conter pelo menos uma letra minúscula")
        if not re.search(r"[0-9]", v):
            raise ValueError("A senha deve conter pelo menos um número")
        if not re.search(r"[!@#$]", v):
            raise ValueError("A senha deve conter pelo menos um dos caracteres: !@#$")
        return v

class UsuarioOut(UsuarioBase):
    id: str
    email_confirmado: int
    criado_em: datetime
    atualizado_em: datetime


class UsuarioLogin(BaseModel):
    email: EmailStr
    senha: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
