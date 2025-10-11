from sqlalchemy.orm import Session
from app.models.extra_models import Extra
from app.schemas.extra_schemas import ExtraCreate, ExtraUpdate
from uuid import UUID

def get_extras(db: Session):
    return db.query(Extra).all()

def get_extra(db: Session, extra_id: str | UUID):
    return db.query(Extra).filter(Extra.id == str(UUID(str(extra_id)))).first()

def create_extra(db: Session, extra: ExtraCreate):
    novo_extra = Extra(**extra.model_dump())
    db.add(novo_extra)
    db.commit()
    db.refresh(novo_extra)
    return novo_extra

def update_extra(db: Session, extra_id: str | UUID, extra_data: ExtraUpdate):
    extra = db.query(Extra).filter(Extra.id == str(UUID(str(extra_id)))).first()
    if not extra:
        return None

    for key, value in extra_data.model_dump(exclude_unset=True).items():
        setattr(extra, key, value)

    db.commit()
    db.refresh(extra)
    return extra

def delete_extra(db: Session, extra_id: str | UUID):
    extra = db.query(Extra).filter(Extra.id == str(UUID(str(extra_id)))).first()
    if not extra:
        return None
    db.delete(extra)
    db.commit()
    return True
