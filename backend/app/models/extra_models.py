from sqlalchemy import Column, Integer,Numeric, String, ForeignKey, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
from app.database import Base
import uuid

class Extra(Base):
    __tablename__ = "extras"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nome = Column(String(100), nullable=False)
    preco = Column(Numeric(10, 2), nullable=False)
    descricao = Column(String(255), nullable=False)
    kcal = Column(Numeric(10, 1), nullable=True)
    peso = Column(Numeric(10, 1), nullable=False)
    imagem_url = Column(String(255), nullable=False)
    estrela = Column(Integer, nullable=True)
    legenda = Column(String(100), nullable=False)

    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)