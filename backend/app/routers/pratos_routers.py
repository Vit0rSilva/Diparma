from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import prato_schemas, response_schemas
from app.repositories import prato_repositories
from app.deps import get_current_administrador, get_db
from uuid import UUID

router = APIRouter(prefix="/pratos", tags=["Pratos"])


@router.get("/", response_model=response_schemas.SuccessResponse)
def listar_pratos(db: Session = Depends(get_db)):
    tipos_pratos = prato_repositories.get_pratos(db)

    # Converter cada item para o schema de resposta
    tipos_pratos_data = [
        prato_schemas.PratoResponse.model_validate(tb).model_dump()
        for tb in tipos_pratos
    ]

    return response_schemas.SuccessResponse(
        message = "Listando todos os tipos",
        data = tipos_pratos_data
    )


@router.get("/{prato_id}", response_model=response_schemas.SuccessResponse)
def prato_por_id(prato_id: UUID, db: Session = Depends(get_db)):
    prato = prato_repositories.get_prato(db, prato_id)
    if not prato:
            raise HTTPException(status_code=404, detail={"message": "Tipo de prato não encontrado", "error_code": "NOT_FOUND_PRATO"})

    prato_data = prato_schemas.PratoResponse.model_validate(prato).model_dump()
    
    return response_schemas.SuccessResponse(
        message = "Valor encontrado",
        data = prato_data
    )


@router.post("/", response_model=response_schemas.SuccessResponse)
def criar_prato(
    prato: prato_schemas.PratoCreate,
    db: Session = Depends(get_db)
):
    if not prato:
        raise HTTPException(status_code=400, detail="Dados inválidos")

    novo_prato = prato_repositories.create_prato(db, prato)

    return response_schemas.SuccessResponse(
        message="Tipo de prato criado com sucesso.",
        data= prato_schemas.PratoResponse.model_validate(novo_prato)
    )


@router.put("/{prato_id}", response_model=response_schemas.SuccessResponse)
def atualizar_prato(
    prato_id: UUID,
    prato_data: prato_schemas.PratoUpdate,
    db: Session = Depends(get_db)
):
    prato_atualizado = prato_repositories.update_prato(
        db, prato_id, prato_data
    )

    if not prato_atualizado:
        raise HTTPException(status_code=404, detail={"message": "Tipo de prato não encontrado", "error_code": "NOT_FOUND_PRATO"})

    return response_schemas.SuccessResponse(
        message="Tipo de prato atualizado com sucesso.",
        data=prato_schemas.PratoResponse.model_validate(prato_atualizado)
    )

@router.delete("/{prato_id}", response_model=response_schemas.SuccessResponse)
def deletar_prato(prato_id: UUID, db: Session = Depends(get_db), adm = Depends(get_current_administrador)):
    prato = prato_repositories.get_prato(db, prato_id)
    if not prato:
        raise HTTPException(status_code=404, detail={"message": "Tipo de prato não encontrado", "error_code": "NOT_FOUND_PRATO"})

    db.delete(prato)
    db.commit()

    return response_schemas.SuccessResponse(
        message="Tipo de prato deletado com sucesso.",
        data=False
    )