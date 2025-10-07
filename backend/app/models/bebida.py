from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime
import uuid
from sqlalchemy.orm import relationship
from app.database import Base

class Bebida(Base):
    __tablename__ = "bebidas"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nome = Column(String(100), nullable=False)
    preco = Column(Integer, nullable=False)
    precoDesconto = Column(Integer, nullable=True)
    desconto = Column(Integer, default=0)
    descricao = Column(String(255), nullable=False)
    imagem_url = Column(String(255), nullable=False)
    estrela = Column(Integer, nullable=True)
    legenda = Column(String(100), nullable=False)
    unidadeMedida = Column(Integer, nullable=False)

    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    tipo_bebida_id = Column(Integer, ForeignKey("enum_tipo_bebida.id"), nullable=False)
    tipo_bebida = relationship("TipoBebida", back_populates="bebida")