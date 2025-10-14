import uuid
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
from app.models.endereco_models import Enderecos

class Usuarios(Base):
    __tablename__ = "usuarios"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    email_confirmado = Column(Integer, default=0)
    telefone = Column(String(20), nullable=True)
    cpf = Column(String(11), unique=True, nullable=False)
    senha = Column(String(255), nullable=False)
    relembrar_token = Column(String(255), nullable=True)

    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    enderecos = relationship("Enderecos", back_populates="usuario", cascade="all, delete-orphan")
    carrinhos = relationship("Carrinho", back_populates="usuario", cascade="all, delete-orphan")
    pedidos = relationship("Pedido", back_populates="usuario", cascade="all, delete-orphan")
