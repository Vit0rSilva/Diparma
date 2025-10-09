# app/schemas/administrador.py
from pydantic import BaseModel, EmailStr, field_validator, validator, constr
from typing import Optional
from datetime import datetime
import re

class AdministradorBase(BaseModel):
    nome: constr(min_length=2, max_length=100)
    cpf: constr(min_length=11, max_length=11, pattern=r"^\d{11}$")
    email: EmailStr

class AdministradorCreate(AdministradorBase):
    senha: constr(min_length=8, max_length=128)

    @field_validator("senha")
    @classmethod
    def senha_regras(cls, v: str) -> str:
        # validações de senha — personalize conforme desejar
        if not re.search(r"[A-Z]", v):
            raise ValueError("A senha deve conter pelo menos uma letra maiúscula")
        if not re.search(r"[a-z]", v):
            raise ValueError("A senha deve conter pelo menos uma letra minúscula")
        if not re.search(r"[0-9]", v):
            raise ValueError("A senha deve conter pelo menos um número")
        if not re.search(r"[!@#$]", v):
            raise ValueError("A senha deve conter pelo menos um dos caracteres: !@#$")
        # Argon2 não tem limite de 72 bytes, então não truncamos aqui.
        return v

class AdministradorOut(AdministradorBase):
    id: str
    ativo: bool
    api_token: str
    criado_em: datetime
    atualizado_em: datetime

    model_config = {"from_attributes": True}  # permite validar direto a partir da instância ORM

class AdministradorLogin(BaseModel):
    email: EmailStr
    senha: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int  # segundos