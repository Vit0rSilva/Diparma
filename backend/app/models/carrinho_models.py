from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
import uuid

class Carrinho(Base):
    __tablename__ = "carrinhos"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    usuario_id = Column(String(36), ForeignKey("usuarios.id"), nullable=False)
    status = Column(String(30), nullable=False, default="aberto")  # aberto, fechado

    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    usuario = relationship("Usuarios", back_populates="carrinhos")
    itens = relationship("CarrinhoItem", back_populates="carrinho", cascade="all, delete-orphan")

class CarrinhoItem(Base):
    __tablename__ = "carrinho_itens"

    id = Column(Integer, primary_key=True, autoincrement=True)
    carrinho_id = Column(String(36), ForeignKey("carrinhos.id"), nullable=False)

    prato_id = Column(String(36), ForeignKey("pratos.id"), nullable=True)
    bebida_id = Column(String(36), ForeignKey("bebidas.id"), nullable=True)
    extra_id = Column(String(36), ForeignKey("extras.id"), nullable=True)

    quantidade_prato = Column(Integer, nullable=False, default=1)
    quantidade_bebida = Column(Integer, nullable=False, default=0)
    quantidade_extra = Column(Integer, nullable=False, default=0)

    preco_unitario = Column(Numeric(10,2), nullable=False)  # preco base do item (prato+bebida+extras) calculado no backend
    subtotal = Column(Numeric(10,2), nullable=False)  # preco_unitario * quantidade_total

    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    carrinho = relationship("Carrinho", back_populates="itens")
    prato = relationship("Prato")
    bebida = relationship("Bebida")
    extra = relationship("Extra")
