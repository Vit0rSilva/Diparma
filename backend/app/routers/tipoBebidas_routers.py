from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import tipoBebidas_schemas, response_schemas
from app.repositories import tipoBebida_repositories
from app.deps import get_current_administrador, get_db

router = APIRouter(prefix="/tipo_bebidas", tags=["Tipo Bebidas"])


@router.get("/", response_model=response_schemas.SuccessResponse)
def listar_tipo_bebidas(db: Session = Depends(get_db)):
    tipos_bebidas = tipoBebida_repositories.get_tipo_bebidas(db)

    # Converter cada item para o schema de resposta
    tipos_bebidas_data = [
        tipoBebidas_schemas.TipoBebidaResponse.model_validate(tb).model_dump()
        for tb in tipos_bebidas
    ]

    return response_schemas.SuccessResponse(
        message = "Listando todos os tipos",
        data = tipos_bebidas_data
    )


@router.get("/{tipo_bebida_id}", response_model=response_schemas.SuccessResponse)
def tipo_bebida_por_id(tipo_bebida_id: int, db: Session = Depends(get_db)):
    tipo_bebida = tipoBebida_repositories.get_tipo_bebida(db, tipo_bebida_id)
    if not tipo_bebida:
        raise HTTPException(status_code=404, detail="Tipo de bebida não encontrado")

    tipo_bebida_data = tipoBebidas_schemas.TipoBebidaResponse.model_validate(tipo_bebida).model_dump()
    
    return response_schemas.SuccessResponse(
        message = "Valor encontrado",
        data = tipo_bebida_data
    )


@router.post("/", response_model=response_schemas.SuccessResponse)
def criar_tipo_bebida(
    tipo_bebida: tipoBebidas_schemas.TipoBebidaCreate,
    db: Session = Depends(get_db)
):
    if not tipo_bebida:
        raise HTTPException(status_code=400, detail="Dados inválidos")

    novo_tipo_bebida = tipoBebida_repositories.create_tipo_bebida(db, tipo_bebida)
    data = tipoBebidas_schemas.TipoBebidaResponse.model_validate(novo_tipo_bebida).model_dump()

    return response_schemas.SuccessResponse(
        message="Tipo de bebida criado com sucesso.",
        data=data
    )


@router.put("/{tipo_bebida_id}", response_model=response_schemas.SuccessResponse)
def atualizar_tipo_bebida(
    tipo_bebida_id: int,
    tipo_bebida_data: tipoBebidas_schemas.TipoBebibaUpdate,
    db: Session = Depends(get_db)
):
    tipo_bebida_atualizado = tipoBebida_repositories.update_tipo_bebida(
        db, tipo_bebida_id, tipo_bebida_data
    )

    if not tipo_bebida_atualizado:
        raise HTTPException(status_code=404, detail="Tipo de bebida não encontrado")
    
    data = tipoBebidas_schemas.TipoBebidaResponse.model_validate(tipo_bebida_atualizado).model_dump()

    return response_schemas.SuccessResponse(
        message="Tipo de bebida atualizado com sucesso.",
        data=data
    )

@router.delete("/{tipo_bebida_id}", response_model=response_schemas.SuccessResponse)
def deletar_tipo_bebida(tipo_bebida_id: int, db: Session = Depends(get_db), current_admin = Depends(get_current_administrador)):
    tipo_bebida = tipoBebida_repositories.get_tipo_bebida(db, tipo_bebida_id)
    if not tipo_bebida:
        raise HTTPException(status_code=404, detail={"message": "Tipo de bebida não encontrado", "error_code": "TIPO_BEBIDA_NOT_FOUND"})

    db.delete(tipo_bebida)
    db.commit()

    return response_schemas.SuccessResponse(
        message="Tipo de bebida deletado com sucesso.",
        data=False
    )