from sqlalchemy import Column, String, Integer, Numeric, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base
from app.models.endereco_models import Enderecos
import uuid

class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    usuario_id = Column(String(36), ForeignKey("usuarios.id"), nullable=False)
    carrinho_id = Column(String(36), ForeignKey("carrinhos.id"), nullable=False)

    status = Column(String(50), default="em_andamento", nullable=False)
    total = Column(Numeric(10, 2), nullable=False)

    # 🔹 novos campos solicitados
    frete = Column(Numeric(10, 2), nullable=True)
    retirada_boll = Column(Boolean, default=False)  # True = retirada; False = entrega
    horario_retirada = Column(String(50), nullable=True)
    observacao = Column(String(255), nullable=True)

    # 🔹 vínculo com endereço do usuário
    id_endereco = Column(String(36), ForeignKey("enderecos.id"), nullable=True)
    endereco = relationship("Enderecos")

    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    usuario = relationship("Usuarios", back_populates="pedidos")
    itens = relationship("PedidoItem", back_populates="pedido")


class PedidoItem(Base):
    __tablename__ = "pedido_itens"

    id = Column(Integer, primary_key=True, autoincrement=True)
    pedido_id = Column(String(36), ForeignKey("pedidos.id"), nullable=False)

    nome = Column(String(255), nullable=False)  # congelado
    quantidade = Column(Integer, nullable=False)
    preco_unitario = Column(Numeric(10,2), nullable=False)
    subtotal = Column(Numeric(10,2), nullable=False)

    criado_em = Column(DateTime, default=datetime.utcnow)

    pedido = relationship("Pedido", back_populates="itens")
