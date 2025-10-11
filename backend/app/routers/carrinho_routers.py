# app/api/carrinhos.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas import item_schemas, carrinho_schemas, response_schemas
from app.repositories import item_repositories
from app.deps import get_db, get_current_usuario
from uuid import UUID

router = APIRouter(prefix="/carrinhos", tags=["Carrinho"])

@router.post("/", response_model=response_schemas.SuccessResponse, status_code=status.HTTP_201_CREATED)
def adicionar_ao_carrinho(payload: item_schemas.ItemCreate, db: Session = Depends(get_db), usuario = Depends(get_current_usuario)):
    novo_item, carrinho_or_err = item_repositories.add_to_cart(db, usuario.id, payload)
    if novo_item is None:
        # carrinho_or_err é dicionário de erro
        raise HTTPException(status_code=400, detail=carrinho_or_err)

    # Formata saída: retorna a entrada do carrinho (se existir) ou o item criado com um objeto carrinho
    # Se foi encontrado existing_carrinho, carrinho_or_err será a instância de Carrinho; mas o repositório pode retornar (item, carrinho)
    # Aqui vamos montar uma resposta simples: retornar o item criado/atualizado
    item_resp = item_schemas.ItemResponse.model_validate(novo_item).model_dump()
    return response_schemas.SuccessResponse(message="Item adicionado/atualizado no carrinho", data=item_resp)

@router.get("/", response_model=response_schemas.SuccessResponse)
def listar_carrinho(db: Session = Depends(get_db), usuario = Depends(get_current_usuario)):
    entries = item_repositories.list_cart_for_user(db, usuario.id)
    # entries são instâncias de Carrinho com relationship.item carregado (se lazy, SQLAlchemy faz lazy load)
    data = []
    for e in entries:
        # montar CarrinhoResponse
        carrinho_data = carrinho_schemas.CarrinhoResponse.model_validate(e).model_dump()
        data.append(carrinho_data)

    return response_schemas.SuccessResponse(
        message="Listando itens do carrinho",
        data={"itens": data, "total_itens": len(data)}
    )

@router.put("/{carrinho_id}", response_model=response_schemas.SuccessResponse)
def atualizar_item_carrinho(carrinho_id: UUID, payload: item_schemas.ItemUpdate, db: Session = Depends(get_db), usuario = Depends(get_current_usuario)):
    updated = item_repositories.update_cart_item_quantities(db, carrinho_id, usuario.id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail={"message": "Item do carrinho não encontrado", "error_code": "NOT_FOUND_CARRINHO"})
    # retornar carrinho atualizado
    return response_schemas.SuccessResponse(message="Item atualizado com sucesso", data=carrinho_schemas.CarrinhoResponse.model_validate(updated))

@router.delete("/{carrinho_id}", response_model=response_schemas.SuccessResponse)
def remover_item_carrinho(carrinho_id: UUID, db: Session = Depends(get_db), usuario = Depends(get_current_usuario)):
    removed = item_repositories.remove_cart_entry(db, carrinho_id, usuario.id)
    if not removed:
        raise HTTPException(status_code=404, detail={"message": "Item do carrinho não encontrado", "error_code": "NOT_FOUND_CARRINHO"})
    return response_schemas.SuccessResponse(message="Item removido do carrinho", data=False)

@router.delete("/", response_model=response_schemas.SuccessResponse)
def limpar_carrinho(db: Session = Depends(get_db), usuario = Depends(get_current_usuario)):
    item_repositories.clear_cart(db, usuario.id)
    return response_schemas.SuccessResponse(message="Carrinho limpo com sucesso", data=False)
