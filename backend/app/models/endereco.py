from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
from app.database import Base

class Endereco(Base):
    __tablename__ = "enderecos"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    rua = Column(String(255), nullable=False)
    numero = Column(String(10), nullable=False)
    cidade = Column(String(100), nullable=False)
    complemento = Column(String(100), nullable=True)
    cep = Column(String(20), nullable=False)
    lat = Column(String(50), nullable=True)
    lng = Column(String(50), nullable=True)

    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    usuario_id = Column(String(36), ForeignKey("usuarios.id"), nullable=False)
    usuario = relationship("Usuarios", back_populates="enderecos")