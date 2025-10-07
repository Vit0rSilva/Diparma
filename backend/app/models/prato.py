from sqlalchemy import Column, Integer,ForeignKey , String, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
from app.database import Base
import uuid

class Prato(Base):
    __tablename__ = "pratos"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nome = Column(String(100), nullable=False)
    preco = Column(Integer, nullable=False)
    precoDesconto = Column(Integer, nullable=True)
    desconto = Column(Integer, default=0)
    pessoas = Column(Integer, nullable=False)
    kcal = Column(Integer, nullable=True)
    peso = Column(Integer, nullable=False)
    descricao = Column(String(255), nullable=False)
    imagem_url = Column(String(255), nullable=False)
    estrela = Column(Integer, nullable=True)
    legenda = Column(String(100), nullable=True)
    tipo = Column(String(50), nullable=True)

    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    tipo_prato_id = Column(Integer, ForeignKey("enum_tipo_prato.id"), nullable=False)
    tipo_prato = relationship("TipoPrato", back_populates="pratos")