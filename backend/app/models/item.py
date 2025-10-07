from sqlalchemy import Column, Integer, String, ForeignKey, DateTime  
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Item(Base):
    __tablename__ = "itens"

    id = Column(Integer, primary_key=True, autoincrement=True)
    prato_id = Column(String(36), ForeignKey("pratos.id"), nullable=True)
    bebida_id = Column(String(36), ForeignKey("bebidas.id"), nullable=True)
    extra_id = Column(String(36), ForeignKey("extras.id"), nullable=True)
    quantidade = Column(Integer, nullable=False, default=1)

    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    prato = relationship("Prato")
    bebida = relationship("Bebida")
    extra = relationship("Extra")
    carrinhos = relationship("Carrinho", back_populates="item")
    pedidos = relationship("Pedido", back_populates="item")