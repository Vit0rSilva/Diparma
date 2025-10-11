from sqlalchemy.orm import Session, joinedload
from app.schemas.bebida_schemas import BebidaBase, BebidaUpdate, BebidaCreate
from app.models.bebida_models import  Bebida
from uuid import UUID


def get_bebidas(db: Session):
    return db.query(Bebida).all()


def get_bebida(db: Session, bebida_id: str | UUID):
    return db.query(Bebida).filter(
        Bebida.id == str(UUID(str(bebida_id)))
    ).first()


def create_bebida(db: Session, bebida: BebidaCreate):
    nova_bebida = Bebida(**bebida.model_dump())
    db.add(nova_bebida)
    db.commit()
    db.refresh(nova_bebida)
    return nova_bebida


def update_bebida(db: Session, bebida_id: UUID | str, bebida_data: BebidaUpdate):
    bebida = db.query(Bebida).filter(
        Bebida.id == str(UUID(str(bebida_id)))
    ).first()

    if not bebida:
        return None

    for key, value in bebida_data.model_dump(exclude_unset=True).items():
        setattr(bebida, key, value)

    db.commit()
    db.refresh(bebida)
    return bebida