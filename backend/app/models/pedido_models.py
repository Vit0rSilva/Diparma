import uuid
from datetime import datetime
from sqlalchemy import Column, Integer,Numeric , String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base

class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    item_id = Column(Integer, ForeignKey("itens.id"), nullable=False)
    usuario_id = Column(String(36), ForeignKey("usuarios.id"), nullable=False)
    endereco_id = Column(Integer, ForeignKey("enderecos.id"), nullable=False)
    frete = Column(Numeric(10, 2), nullable=True)
    retirada_loja = Column(Integer, nullable=True, default=0)
    retirada_hora = Column(String(50), nullable=True)
    total = Column(Numeric(10, 2), nullable=False)
    status = Column(String(50), nullable=False, default="Pendente")
    observacoes = Column(String(255), nullable=True)

    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    item = relationship("Item", back_populates="pedidos")
    usuario = relationship("Usuarios")
    endereco = relationship("Endereco")