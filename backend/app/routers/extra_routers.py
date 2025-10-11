from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import extra_schemas, response_schemas
from app.repositories import extra_repositories
from app.deps import get_db, get_current_administrador
from uuid import UUID

router = APIRouter(prefix="/extras", tags=["Extras"])

@router.get("/", response_model=response_schemas.SuccessResponse)
def listar_extras(db: Session = Depends(get_db)):
    extras = extra_repositories.get_extras(db)
    extras_data = [
        extra_schemas.ExtraResponse.model_validate(e).model_dump()
        for e in extras
    ]
    return response_schemas.SuccessResponse(
        message="Listando todos os extras.",
        data=extras_data
    )

@router.get("/{extra_id}", response_model=response_schemas.SuccessResponse)
def extra_por_id(extra_id: UUID, db: Session = Depends(get_db)):
    extra = extra_repositories.get_extra(db, extra_id)
    if not extra:
        raise HTTPException(status_code=404, detail={
            "message": "Extra não encontrado.",
            "error_code": "NOT_FOUND_EXTRA"
        })

    return response_schemas.SuccessResponse(
        message="Extra encontrado.",
        data=extra_schemas.ExtraResponse.model_validate(extra)
    )

@router.post("/", response_model=response_schemas.SuccessResponse)
def criar_extra(
    extra: extra_schemas.ExtraCreate,
    db: Session = Depends(get_db),
    adm = Depends(get_current_administrador)
):
    novo_extra = extra_repositories.create_extra(db, extra)
    return response_schemas.SuccessResponse(
        message="Extra criado com sucesso.",
        data=extra_schemas.ExtraResponse.model_validate(novo_extra)
    )

@router.put("/{extra_id}", response_model=response_schemas.SuccessResponse)
def atualizar_extra(
    extra_id: UUID,
    extra_data: extra_schemas.ExtraUpdate,
    db: Session = Depends(get_db),
    adm = Depends(get_current_administrador)
):
    extra_atualizado = extra_repositories.update_extra(db, extra_id, extra_data)
    if not extra_atualizado:
        raise HTTPException(status_code=404, detail={
            "message": "Extra não encontrado.",
            "error_code": "NOT_FOUND_EXTRA"
        })

    return response_schemas.SuccessResponse(
        message="Extra atualizado com sucesso.",
        data=extra_schemas.ExtraResponse.model_validate(extra_atualizado)
    )

@router.delete("/{extra_id}", response_model=response_schemas.SuccessResponse)
def deletar_extra(extra_id: UUID, db: Session = Depends(get_db), adm = Depends(get_current_administrador)):
    extra = extra_repositories.get_extra(db, extra_id)
    if not extra:
        raise HTTPException(status_code=404, detail={
            "message": "Extra não encontrado.",
            "error_code": "NOT_FOUND_EXTRA"
        })
    db.delete(extra)
    db.commit()

    return response_schemas.SuccessResponse(
        message="Extra deletado com sucesso.",
        data=False
    )
