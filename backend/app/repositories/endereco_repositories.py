from sqlalchemy.orm import Session
from app.models.endereco_models import Enderecos
from app.schemas.endereco_schemas import EnderecoCreate, EnderecoUpdate
from uuid import UUID

def get_enderecos_all(db: Session):
    return db.query(Enderecos).all()

def get_enderecos_by_usuario(db: Session, usuario_id: str | UUID):
    return db.query(Enderecos).filter(Enderecos.usuario_id == str(usuario_id)).all()

def get_endereco(db: Session, endereco_id: int, usuario_id: str | UUID):
    return (
        db.query(Enderecos)
        .filter(Enderecos.id == endereco_id, Enderecos.usuario_id == str(usuario_id))
        .first()
    )

def create_endereco(db: Session, endereco: EnderecoCreate, usuario_id: str | UUID):
    novo_endereco = Enderecos(**endereco.model_dump(), usuario_id=str(usuario_id))
    db.add(novo_endereco)
    db.commit()
    db.refresh(novo_endereco)
    return novo_endereco

def update_endereco(db: Session, endereco_id: int, usuario_id: str | UUID, endereco_data: EnderecoUpdate):
    endereco = get_endereco(db, endereco_id, usuario_id)
    if not endereco:
        return None

    for key, value in endereco_data.model_dump(exclude_unset=True).items():
        setattr(endereco, key, value)

    db.commit()
    db.refresh(endereco)
    return endereco

def delete_endereco(db: Session, endereco_id: int, usuario_id: str | UUID):
    endereco = get_endereco(db, endereco_id, usuario_id)
    if not endereco:
        return None
    db.delete(endereco)
    db.commit()
    return True
