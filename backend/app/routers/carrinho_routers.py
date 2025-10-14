# app/api/carrinho.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas import carrinho_schemas, response_schemas
from app.repositories import carrinho_repositories as cart_repo
from app.deps import get_db, get_current_usuario

router = APIRouter(prefix="/carrinho", tags=["Carrinho"])

@router.get("/", response_model=response_schemas.SuccessResponse)
def listar_carrinho(db: Session = Depends(get_db), usuario = Depends(get_current_usuario)):
    cart, items = cart_repo.list_cart_items(db, usuario.id)
    items_data = [carrinho_schemas.CarrinhoItemResponse.model_validate(i).model_dump() for i in items]
    resp = {
        "id": cart.id,
        "usuario_id": cart.usuario_id,
        "status": cart.status,
        "itens": items_data,
        "criado_em": cart.criado_em,
        "atualizado_em": cart.atualizado_em
    }
    totals = cart_repo.get_cart_totals(db, usuario.id)
    resp.update({"total": float(totals["total"]), "total_itens": totals["total_itens"], "items_count": totals["items_count"]})
    return response_schemas.SuccessResponse(message="Carrinho do usuário", data=resp)

@router.post("/", response_model=response_schemas.SuccessResponse, status_code=status.HTTP_201_CREATED)
def adicionar_item(payload: carrinho_schemas.CarrinhoItemCreate, db: Session = Depends(get_db), usuario = Depends(get_current_usuario)):
    novo, err = cart_repo.add_item_to_cart(db, usuario.id, payload)
    if err:
        raise HTTPException(status_code=400, detail=err)
    return response_schemas.SuccessResponse(message="Item adicionado ao carrinho", data=carrinho_schemas.CarrinhoItemResponse.model_validate(novo))

@router.put("/{item_id}", response_model=response_schemas.SuccessResponse)
def atualizar_item(item_id: int, payload: carrinho_schemas.CarrinhoItemUpdate, db: Session = Depends(get_db), usuario = Depends(get_current_usuario)):
    updated = cart_repo.update_cart_item(db, usuario.id, item_id, payload)
    if updated is None:
        raise HTTPException(status_code=404, detail={"message": "Item não encontrado ou removido (quantidade zero)", "error_code": "NOT_FOUND_ITEM"})
    return response_schemas.SuccessResponse(message="Item atualizado", data=carrinho_schemas.CarrinhoItemResponse.model_validate(updated))

@router.delete("/{item_id}", response_model=response_schemas.SuccessResponse)
def remover_item(item_id: int, db: Session = Depends(get_db), usuario = Depends(get_current_usuario)):
    ok = cart_repo.remove_cart_item(db, usuario.id, item_id)
    if not ok:
        raise HTTPException(status_code=404, detail={"message":"Item não encontrado","error_code":"NOT_FOUND_ITEM"})
    return response_schemas.SuccessResponse(message="Item removido", data=False)

@router.delete("/", response_model=response_schemas.SuccessResponse)
def limpar_cart(db: Session = Depends(get_db), usuario = Depends(get_current_usuario)):
    cart_repo.clear_cart(db, usuario.id)
    return response_schemas.SuccessResponse(message="Carrinho limpo", data=False)
