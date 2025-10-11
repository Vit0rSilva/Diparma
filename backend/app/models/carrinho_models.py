from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
import uuid

class Carrinho(Base):
    __tablename__ = "carrinhos"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    item_id = Column(Integer, ForeignKey("itens.id"), nullable=False)
    usuario_id = Column(String(36), ForeignKey("usuarios.id"), nullable=False)

    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    item = relationship("Item")
    usuario = relationship("Usuarios")