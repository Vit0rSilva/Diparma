from sqlalchemy.orm import Session
from app.schemas.tipoPrato_schemas import TipoPratoBase, TipoPratoCreate, TipoPratoResponse, TipoPratoUpdate
from app.models.tipoPrato_models import  TipoPrato

def get_tipo_pratos(db: Session):
    return db.query(TipoPrato).all()


def get_tipo_prato(db: Session, tipo_prato_id: int):
    return db.query(TipoPrato).filter(
        TipoPrato.id == tipo_prato_id
    ).first()


def create_tipo_prato(db: Session, tipo_prato: TipoPratoCreate):
    nova_tipo_prato = TipoPrato(**tipo_prato.model_dump())
    db.add(nova_tipo_prato)
    db.commit()
    db.refresh(nova_tipo_prato)
    return nova_tipo_prato


def update_tipo_prato(db: Session, tipo_prato_id: int, tipo_prato_data: TipoPratoUpdate):
    tipo_prato = db.query(TipoPrato).filter(
        TipoPrato.id == tipo_prato_id
    ).first()

    if not tipo_prato:
        return None

    for key, value in tipo_prato_data.model_dump(exclude_unset=True).items():
        setattr(tipo_prato, key, value)

    db.commit()
    db.refresh(tipo_prato)
    return tipo_prato