from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import tipoPrato_schemas, response_schemas
from app.repositories import tipoPrato_repositories
from app.deps import get_current_administrador, get_db

router = APIRouter(prefix="/tipo_pratos", tags=["Tipo Pratos"])


@router.get("/", response_model=response_schemas.SuccessResponse)
def listar_tipo_pratos(db: Session = Depends(get_db)):
    tipos_pratos = tipoPrato_repositories.get_tipo_pratos(db)

    # Converter cada item para o schema de resposta
    tipos_pratos_data = [
        tipoPrato_schemas.TipoPratoResponse.model_validate(tb).model_dump()
        for tb in tipos_pratos
    ]

    return response_schemas.SuccessResponse(
        message = "Listando todos os tipos",
        data = tipos_pratos_data
    )


@router.get("/{tipo_prato_id}", response_model=response_schemas.SuccessResponse)
def tipo_prato_por_id(tipo_prato_id: int, db: Session = Depends(get_db)):
    tipo_prato = tipoPrato_repositories.get_tipo_prato(db, tipo_prato_id)
    if not tipo_prato:
            raise HTTPException(status_code=404, detail={"message": "Tipo de prato não encontrado", "error_code": "NOT_FOUND_TIPO_PRATO"})

    tipo_prato_data = tipoPrato_schemas.TipoPratoResponse.model_validate(tipo_prato).model_dump()
    
    return response_schemas.SuccessResponse(
        message = "Valor encontrado",
        data = tipo_prato_data
    )


@router.post("/", response_model=response_schemas.SuccessResponse)
def criar_tipo_prato(
    tipo_prato: tipoPrato_schemas.TipoPratoCreate,
    db: Session = Depends(get_db)
):
    if not tipo_prato:
        raise HTTPException(status_code=400, detail="Dados inválidos")

    novo_tipo_prato = tipoPrato_repositories.create_tipo_prato(db, tipo_prato)

    return response_schemas.SuccessResponse(
        message="Tipo de prato criado com sucesso.",
        data=tipoPrato_schemas.TipoPratoResponse.model_validate(novo_tipo_prato)
    )


@router.put("/{tipo_prato_id}", response_model=response_schemas.SuccessResponse)
def atualizar_tipo_prato(
    tipo_prato_id: int,
    tipo_prato_data: tipoPrato_schemas.TipoPratoUpdate,
    db: Session = Depends(get_db)
):
    tipo_prato_atualizado = tipoPrato_repositories.update_tipo_prato(
        db, tipo_prato_id, tipo_prato_data
    )

    if not tipo_prato_atualizado:
        raise HTTPException(status_code=404, detail={"message": "Tipo de prato não encontrado", "error_code": "NOT_FOUND_TIPO_PRATO"})

    return response_schemas.SuccessResponse(
        message="Tipo de prato atualizado com sucesso.",
        data=tipoPrato_schemas.TipoPratoResponse.model_validate(tipo_prato_atualizado)
    )

@router.delete("/{tipo_prato_id}", response_model=response_schemas.SuccessResponse)
def deletar_tipo_prato(tipo_prato_id: int, db: Session = Depends(get_db), adm = Depends(get_current_administrador)):
    tipo_prato = tipoPrato_repositories.get_tipo_prato(db, tipo_prato_id)
    if not tipo_prato:
        raise HTTPException(status_code=404, detail={"message": "Tipo de prato não encontrado", "error_code": "NOT_FOUND_TIPO_PRATO"})

    db.delete(tipo_prato)
    db.commit()

    return response_schemas.SuccessResponse(
        message="Tipo de prato deletado com sucesso.",
        data=False
    )