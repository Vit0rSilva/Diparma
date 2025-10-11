# app/repositories/item_repositories.py
from sqlalchemy.orm import Session
from app.models.item_models import Item
from app.models.carrinho_models import Carrinho
from app.schemas.item_schemas import ItemCreate, ItemUpdate
from uuid import UUID
from sqlalchemy import and_

def find_identical_item_for_user(db: Session, usuario_id: str | UUID, prato_id, bebida_id, extra_id):
    """
    Retorna (item, carrinho) se já existir um item com a mesma combinação
    no carrinho do usuário. Caso contrário, retorna (None, None).
    """
    # join Carrinho -> Item
    q = db.query(Item, Carrinho).join(Carrinho, Carrinho.item_id == Item.id).filter(
        Carrinho.usuario_id == str(usuario_id),
        Item.prato_id == (str(prato_id) if prato_id else None),
        Item.bebida_id == (str(bebida_id) if bebida_id else None),
        Item.extra_id == (str(extra_id) if extra_id else None),
    )
    result = q.first()
    if result:
        return result[0], result[1]
    return None, None

def create_item(db: Session, item_data: ItemCreate):
    novo = Item(
        prato_id = str(item_data.prato_id) if item_data.prato_id else None,
        bebida_id = str(item_data.bebida_id) if item_data.bebida_id else None,
        extra_id = str(item_data.extra_id) if item_data.extra_id else None,
        quantidade_prato = item_data.quantidade_prato,
        quantidade_extra = item_data.quantidade_extra,
    )
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

def create_carrinho_entry(db: Session, usuario_id: str | UUID, item_id: int):
    novo = Carrinho(usuario_id=str(usuario_id), item_id=item_id)
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

def add_to_cart(db: Session, usuario_id: str | UUID, item_payload: ItemCreate):
    # validação básica: deve ter pelo menos um produto
    if not (item_payload.prato_id or item_payload.bebida_id or item_payload.extra_id):
        return None, {"error": "É necessário informar prato_id, bebida_id ou extra_id"}

    # Verifica item idêntico no carrinho do usuário
    existing_item, existing_carrinho = find_identical_item_for_user(
        db, usuario_id, item_payload.prato_id, item_payload.bebida_id, item_payload.extra_id
    )

    if existing_item:
        # atualiza quantidades (soma)
        existing_item.quantidade_prato = (existing_item.quantidade_prato or 0) + (item_payload.quantidade_prato or 0)
        existing_item.quantidade_extra = (existing_item.quantidade_extra or 0) + (item_payload.quantidade_extra or 0)
        db.add(existing_item)
        db.commit()
        db.refresh(existing_item)
        return existing_item, existing_carrinho

    # cria novo item + cria carrinho link
    novo_item = create_item(db, item_payload)
    novo_carrinho = create_carrinho_entry(db, usuario_id, novo_item.id)
    return novo_item, novo_carrinho

def list_cart_for_user(db: Session, usuario_id: str | UUID):
    # retorna todas as entradas do carrinho do usuário com item carregado
    return db.query(Carrinho).filter(Carrinho.usuario_id == str(usuario_id)).all()

def get_carrinho_entry(db: Session, carrinho_id: str | UUID, usuario_id: str | UUID):
    return db.query(Carrinho).filter(
        Carrinho.id == str(carrinho_id),
        Carrinho.usuario_id == str(usuario_id)
    ).first()

def update_cart_item_quantities(db: Session, carrinho_id: str | UUID, usuario_id: str | UUID, item_update: ItemUpdate):
    entry = get_carrinho_entry(db, carrinho_id, usuario_id)
    if not entry:
        return None
    item = entry.item
    if item_update.quantidade_prato is not None:
        item.quantidade_prato = item_update.quantidade_prato
    if item_update.quantidade_extra is not None:
        item.quantidade_extra = item_update.quantidade_extra
    db.add(item)
    db.commit()
    db.refresh(item)
    db.refresh(entry)
    return entry

def remove_cart_entry(db: Session, carrinho_id: str | UUID, usuario_id: str | UUID):
    entry = get_carrinho_entry(db, carrinho_id, usuario_id)
    if not entry:
        return None
    # opcional: remover item também (se você quiser que item não usado permaneça removido)
    item = entry.item
    db.delete(entry)
    db.commit()
    # tenta remover item se não houver mais referências em carrinhos
    still_used = db.query(Carrinho).filter(Carrinho.item_id == item.id).first()
    if not still_used:
        db.delete(item)
        db.commit()
    return True

def clear_cart(db: Session, usuario_id: str | UUID):
    entries = db.query(Carrinho).filter(Carrinho.usuario_id == str(usuario_id)).all()
    item_ids = [e.item_id for e in entries]
    for e in entries:
        db.delete(e)
    db.commit()
    # remove items órfãos
    for iid in set(item_ids):
        still = db.query(Carrinho).filter(Carrinho.item_id == iid).first()
        if not still:
            it = db.query(Item).filter(Item.id == iid).first()
            if it:
                db.delete(it)
    db.commit()
    return True
