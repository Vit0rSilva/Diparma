from sqlalchemy import Column,Boolean,Numeric, Integer, String, ForeignKey, DateTime
from datetime import datetime
import uuid
from sqlalchemy.orm import relationship
from app.database import Base

class Bebida(Base):
    __tablename__ = "bebidas"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nome = Column(String(100), nullable=False)
    preco = Column(Numeric(10, 2), nullable=False)
    precoDesconto = Column(Numeric(10, 2), nullable=True)
    desconto = Column(Boolean, default=False)
    descricao = Column(String(255), nullable=False)
    imagem_url = Column(String(255), nullable=False)
    estrela = Column(Integer, nullable=True)
    legenda = Column(String(100), nullable=False)
    unidadeMedida = Column(Numeric(10, 1), nullable=False)

    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    tipo_bebida_id = Column(Integer, ForeignKey("enum_tipo_bebida.id"), nullable=False)
    tipo_bebida = relationship("TipoBebida", back_populates="bebida")