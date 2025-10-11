from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import endereco_schemas, response_schemas
from app.repositories import endereco_repositories
from app.deps import get_db, get_current_usuario

router = APIRouter(prefix="/enderecos", tags=["Endereços"])

@router.get("/", response_model=response_schemas.SuccessResponse)
def listar_enderecos(db: Session = Depends(get_db)):
    enderecos = endereco_repositories.get_enderecos_all(db)
    enderecos_data = [
        endereco_schemas.EnderecoResponse.model_validate(e).model_dump()
        for e in enderecos
    ]

    return response_schemas.SuccessResponse(
        message="Listando todos os endereços do usuário.",
        data=enderecos_data
    )

@router.get("/{endereco_id}", response_model=response_schemas.SuccessResponse)
def endereco_por_id(endereco_id: int, db: Session = Depends(get_db), usuario = Depends(get_current_usuario)):
    endereco = endereco_repositories.get_endereco(db, endereco_id, usuario.id)
    if not endereco:
        raise HTTPException(status_code=404, detail={"message": "Endereço não encontrado", "error_code": "NOT_FOUND_ENDERECO"})

    return response_schemas.SuccessResponse(
        message="Endereço encontrado com sucesso.",
        data=endereco_schemas.EnderecoResponse.model_validate(endereco)
    )

@router.post("/", response_model=response_schemas.SuccessResponse)
def criar_endereco(endereco: endereco_schemas.EnderecoCreate, db: Session = Depends(get_db), usuario = Depends(get_current_usuario)):
    novo_endereco = endereco_repositories.create_endereco(db, endereco, usuario.id)

    return response_schemas.SuccessResponse(
        message="Endereço criado com sucesso.",
        data=endereco_schemas.EnderecoResponse.model_validate(novo_endereco)
    )

@router.put("/{endereco_id}", response_model=response_schemas.SuccessResponse)
def atualizar_endereco(endereco_id: int, endereco_data: endereco_schemas.EnderecoUpdate, db: Session = Depends(get_db), usuario = Depends(get_current_usuario)):
    endereco_atualizado = endereco_repositories.update_endereco(db, endereco_id, usuario.id, endereco_data)

    if not endereco_atualizado:
        raise HTTPException(status_code=404, detail={"message": "Endereço não encontrado", "error_code": "NOT_FOUND_ENDERECO"})

    return response_schemas.SuccessResponse(
        message="Endereço atualizado com sucesso.",
        data=endereco_schemas.EnderecoResponse.model_validate(endereco_atualizado)
    )

@router.delete("/{endereco_id}", response_model=response_schemas.SuccessResponse)
def deletar_endereco(endereco_id: int, db: Session = Depends(get_db), usuario = Depends(get_current_usuario)):
    deletado = endereco_repositories.delete_endereco(db, endereco_id, usuario.id)
    if not deletado:
        raise HTTPException(status_code=404, detail={"message": "Endereço não encontrado", "error_code": "NOT_FOUND_ENDERECO"})

    return response_schemas.SuccessResponse(
        message="Endereço deletado com sucesso.",
        data=False
    )
