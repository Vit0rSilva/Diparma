from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID
import secrets

from app.models.administrador_models import Administrador
from app.schemas.administrador_shemas import AdministradorCreate


class AdministradorRepository:
    def __init__(self, db: Session):
        self.db = db

    # Buscar por email
    def get_by_email(self, email: str) -> Optional[Administrador]:
        return self.db.query(Administrador).filter(Administrador.email == email).first()

    # Buscar por CPF
    def get_by_cpf(self, cpf: str) -> Optional[Administrador]:
        return self.db.query(Administrador).filter(Administrador.cpf == cpf).first()

    # Buscar por ID (corrigido para UUID)
    def get_by_id(self, id: str | UUID) -> Optional[Administrador]:
        try:
            id_str = str(UUID(str(id)))  # garante formato com hífens
        except (ValueError, TypeError):
            return None
        return self.db.query(Administrador).filter(Administrador.id == id_str).first()

    # Criar novo administrador
    def create(
        self,
        admin_create: AdministradorCreate,
        hashed_password: str,
        api_token: Optional[str] = None
    ) -> Administrador:

        if api_token is None:
            api_token = secrets.token_urlsafe(32)

        admin = Administrador(
            nome=admin_create.nome,
            cpf=admin_create.cpf,
            email=admin_create.email,
            senha=hashed_password,
            api_token=api_token,
            ativo=True
        )

        self.db.add(admin)
        self.db.commit()
        self.db.refresh(admin)
        return admin

    # Atualizar dados do administrador
    def update(self, admin: Administrador) -> Administrador:
        self.db.add(admin)
        self.db.commit()
        self.db.refresh(admin)
        return admin
