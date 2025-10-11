from sqlalchemy.orm import Session, joinedload
from app.schemas.prato_schemas import PratoBase, PratoUpdate, PratoCreate
from app.models.prato_models import  Prato
from uuid import UUID


def get_pratos(db: Session):
    return db.query(Prato).all()


def get_prato(db: Session, prato_id: str | UUID):
    return db.query(Prato).filter(
        Prato.id == str(UUID(str(prato_id)))
    ).first()


def create_prato(db: Session, prato: PratoCreate):
    nova_prato = Prato(**prato.model_dump())
    db.add(nova_prato)
    db.commit()
    db.refresh(nova_prato)
    return nova_prato


def update_prato(db: Session, prato_id: UUID | str, prato_data: PratoUpdate):
    prato = db.query(Prato).filter(
        Prato.id == str(UUID(str(prato_id)))
    ).first()

    if not prato:
        return None

    for key, value in prato_data.model_dump(exclude_unset=True).items():
        setattr(prato, key, value)

    db.commit()
    db.refresh(prato)
    return prato