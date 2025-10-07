from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
from app.database import Base
import uuid

class Extra(Base):
    __tablename__ = "extras"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nome = Column(String(100), nullable=False)
    preco = Column(Integer, nullable=False)
    descricao = Column(String(255), nullable=False)
    kcal = Column(Integer, nullable=True)
    peso = Column(Integer, nullable=False)
    imagem_url = Column(String(255), nullable=False)
    estrela = Column(Integer, nullable=True)
    legenda = Column(String(100), nullable=False)
    tipo = Column(String(50), nullable=True)

    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)