# app/repositories/usuario_repositories.py
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID
import secrets

from app.models.usuario_models import Usuarios
from app.schemas.usuario_schemas import UsuarioCreate

class UsuarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_email(self, email: str) -> Optional[Usuarios]:
        return self.db.query(Usuarios).filter(Usuarios.email == email).first()

    def get_by_cpf(self, cpf: str) -> Optional[Usuarios]:
        return self.db.query(Usuarios).filter(Usuarios.cpf == cpf).first()

    def get_by_id(self, id: str | UUID) -> Optional[Usuarios]:
        try:
            id_str = str(UUID(str(id)))
        except (ValueError, TypeError):
            return None
        return self.db.query(Usuarios).filter(Usuarios.id == id_str).first()

    def create(self, usuario_create: UsuarioCreate, hashed_password: str) -> Usuarios:
        usuario = Usuarios(
            nome=usuario_create.nome,
            cpf=usuario_create.cpf,
            email=usuario_create.email,
            telefone=usuario_create.telefone,
            senha=hashed_password,
            email_confirmado=0
        )
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def update(self, usuario: Usuarios) -> Usuarios:
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario
