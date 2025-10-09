from sqlalchemy.orm import Session
from app.models import tipoBebida_models
from app.schemas import tipoBebidas_schemas

def get_tipo_bebidas(db: Session):
    return db.query(tipoBebida_models.TipoBebida).all()


def get_tipo_bebida(db: Session, tipo_bebida_id: int):
    return db.query(tipoBebida_models.TipoBebida).filter(
        tipoBebida_models.TipoBebida.id == tipo_bebida_id
    ).first()


def create_tipo_bebida(db: Session, tipo_bebida: tipoBebidas_schemas.TipoBebidaCreate):
    nova_tipo_bebida = tipoBebida_models.TipoBebida(**tipo_bebida.model_dump())
    db.add(nova_tipo_bebida)
    db.commit()
    db.refresh(nova_tipo_bebida)
    return nova_tipo_bebida


def update_tipo_bebida(db: Session, tipo_bebida_id: int, tipo_bebida_data: tipoBebidas_schemas.TipoBebibaUpdate):
    tipo_bebida = db.query(tipoBebida_models.TipoBebida).filter(
        tipoBebida_models.TipoBebida.id == tipo_bebida_id
    ).first()

    if not tipo_bebida:
        return None

    for key, value in tipo_bebida_data.model_dump(exclude_unset=True).items():
        setattr(tipo_bebida, key, value)

    db.commit()
    db.refresh(tipo_bebida)
    return tipo_bebida
