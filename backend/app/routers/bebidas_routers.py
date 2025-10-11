from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import bebida_schemas, response_schemas
from app.repositories import bebida_repositories
from app.deps import get_current_administrador, get_db
from uuid import UUID

router = APIRouter(prefix="/bebidas", tags=["Bebidas"])


@router.get("/", response_model=response_schemas.SuccessResponse)
def listar_bebidas(db: Session = Depends(get_db)):
    tipos_bebidas = bebida_repositories.get_bebidas(db)

    # Converter cada item para o schema de resposta
    tipos_bebidas_data = [
        bebida_schemas.BebidaResponse.model_validate(tb).model_dump()
        for tb in tipos_bebidas
    ]

    return response_schemas.SuccessResponse(
        message = "Listando todos os tipos",
        data = tipos_bebidas_data
    )


@router.get("/{bebida_id}", response_model=response_schemas.SuccessResponse)
def bebida_por_id(bebida_id: UUID, db: Session = Depends(get_db)):
    bebida = bebida_repositories.get_bebida(db, bebida_id)
    if not bebida:
            raise HTTPException(status_code=404, detail={"message": "Tipo de bebida não encontrado", "error_code": "NOT_FOUND_BEBIDA"})

    bebida_data = bebida_schemas.BebidaResponse.model_validate(bebida).model_dump()
    
    return response_schemas.SuccessResponse(
        message = "Valor encontrado",
        data = bebida_data
    )


@router.post("/", response_model=response_schemas.SuccessResponse)
def criar_bebida(
    bebida: bebida_schemas.BebidaCreate,
    db: Session = Depends(get_db)
):
    if not bebida:
        raise HTTPException(status_code=400, detail="Dados inválidos")

    novo_bebida = bebida_repositories.create_bebida(db, bebida)

    return response_schemas.SuccessResponse(
        message="Tipo de bebida criado com sucesso.",
        data= bebida_schemas.BebidaResponse.model_validate(novo_bebida)
    )


@router.put("/{bebida_id}", response_model=response_schemas.SuccessResponse)
def atualizar_bebida(
    bebida_id: UUID,
    bebida_data: bebida_schemas.BebidaUpdate,
    db: Session = Depends(get_db)
):
    bebida_atualizado = bebida_repositories.update_bebida(
        db, bebida_id, bebida_data
    )

    if not bebida_atualizado:
        raise HTTPException(status_code=404, detail={"message": "Tipo de bebida não encontrado", "error_code": "NOT_FOUND_BEBIDA"})

    return response_schemas.SuccessResponse(
        message="Tipo de bebida atualizado com sucesso.",
        data=bebida_schemas.BebidaResponse.model_validate(bebida_atualizado)
    )

@router.delete("/{bebida_id}", response_model=response_schemas.SuccessResponse)
def deletar_bebida(bebida_id: UUID, db: Session = Depends(get_db), adm = Depends(get_current_administrador)):
    bebida = bebida_repositories.get_bebida(db, bebida_id)
    if not bebida:
        raise HTTPException(status_code=404, detail={"message": "Tipo de bebida não encontrado", "error_code": "NOT_FOUND_BEBIDA"})

    db.delete(bebida)
    db.commit()

    return response_schemas.SuccessResponse(
        message="Tipo de bebida deletado com sucesso.",
        data=False
    )