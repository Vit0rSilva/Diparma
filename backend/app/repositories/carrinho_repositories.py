# app/repositories/carrinho_repositories.py
from sqlalchemy.orm import Session, joinedload
from app.models.carrinho_models import Carrinho, CarrinhoItem
from app.models.prato_models import Prato
from app.models.bebida_models import Bebida
from app.models.extra_models import Extra
from app.schemas.carrinho_schemas import CarrinhoItemCreate, CarrinhoItemUpdate
from uuid import UUID
from decimal import Decimal

def _str_uuid(v):
    return str(v) if v is not None else None

def get_open_cart_for_user(db: Session, usuario_id: str | UUID) -> Carrinho:
    cart = db.query(Carrinho).filter(Carrinho.usuario_id == str(usuario_id), Carrinho.status == "aberto").first()
    if not cart:
        cart = Carrinho(usuario_id=str(usuario_id))
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart

def list_cart_items(db: Session, usuario_id: str | UUID):
    cart = get_open_cart_for_user(db, usuario_id)
    items = (
        db.query(CarrinhoItem)
        .options(joinedload(CarrinhoItem.prato), joinedload(CarrinhoItem.bebida), joinedload(CarrinhoItem.extra))
        .filter(CarrinhoItem.carrinho_id == cart.id)
        .all()
    )
    return cart, items

def find_similar_item(db: Session, cart_id: str, prato_id, bebida_id, extra_id):
    return db.query(CarrinhoItem).filter(
        CarrinhoItem.carrinho_id == cart_id,
        CarrinhoItem.prato_id == _str_uuid(prato_id),
        CarrinhoItem.bebida_id == _str_uuid(bebida_id),
        CarrinhoItem.extra_id == _str_uuid(extra_id)
    ).first()

def compute_unit_price(db: Session, prato_id, bebida_id, extra_id) -> Decimal:
    total = Decimal("0")
    if prato_id:
        p = db.query(Prato).filter(Prato.id == str(prato_id)).first()
        if p:
            total += Decimal(str(p.preco))
    if bebida_id:
        b = db.query(Bebida).filter(Bebida.id == str(bebida_id)).first()
        if b:
            total += Decimal(str(b.preco))
    if extra_id:
        e = db.query(Extra).filter(Extra.id == str(extra_id)).first()
        if e:
            total += Decimal(str(e.preco))
    return total

def add_item_to_cart(db: Session, usuario_id: str | UUID, payload: CarrinhoItemCreate):
    cart = get_open_cart_for_user(db, usuario_id)

    # validação: pelo menos um dos ids deve ser informado
    if not (payload.prato_id or payload.bebida_id or payload.extra_id):
        return None, {"message": "Informe prato_id ou bebida_id ou extra_id", "error_code": "INVALID_ITEM"}

    # normalize quantities (inteiros >= 0)
    q_prato = int(payload.quantidade_prato or 0)
    q_bebida = int(payload.quantidade_bebida or 0)
    q_extra = int(payload.quantidade_extra or 0)

    if q_prato + q_bebida + q_extra <= 0:
        return None, {"message": "Quantidade total deve ser maior que zero", "error_code": "INVALID_QUANTITY"}

    # tenta encontrar item idêntico no carrinho (mesma combinação de ids)
    existing = find_similar_item(db, cart.id, payload.prato_id, payload.bebida_id, payload.extra_id)
    if existing:
        # soma quantidades por tipo
        existing.quantidade_prato += q_prato
        existing.quantidade_bebida += q_bebida
        existing.quantidade_extra += q_extra

        unit = compute_unit_price(db, existing.prato_id, existing.bebida_id, existing.extra_id)
        total_qty = existing.quantidade_prato + existing.quantidade_bebida + existing.quantidade_extra
        existing.preco_unitario = unit
        existing.subtotal = unit * Decimal(total_qty)

        db.add(existing)
        db.commit()
        db.refresh(existing)
        return existing, None

    # criar novo item
    unit = compute_unit_price(db, payload.prato_id, payload.bebida_id, payload.extra_id)
    total_qty = q_prato + q_bebida + q_extra
    novo = CarrinhoItem(
        carrinho_id = cart.id,
        prato_id = _str_uuid(payload.prato_id),
        bebida_id = _str_uuid(payload.bebida_id),
        extra_id = _str_uuid(payload.extra_id),
        quantidade_prato = q_prato,
        quantidade_bebida = q_bebida,
        quantidade_extra = q_extra,
        preco_unitario = unit,
        subtotal = unit * Decimal(total_qty),
    )
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo, None

def update_cart_item(db: Session, usuario_id: str | UUID, item_id: int, payload: CarrinhoItemUpdate):
    cart = get_open_cart_for_user(db, usuario_id)
    item = db.query(CarrinhoItem).filter(CarrinhoItem.id == item_id, CarrinhoItem.carrinho_id == cart.id).first()
    if not item:
        return None
    if payload.quantidade_prato is not None:
        item.quantidade_prato = int(payload.quantidade_prato)
    if payload.quantidade_bebida is not None:
        item.quantidade_bebida = int(payload.quantidade_bebida)
    if payload.quantidade_extra is not None:
        item.quantidade_extra = int(payload.quantidade_extra)

    total_qty = item.quantidade_prato + item.quantidade_bebida + item.quantidade_extra
    if total_qty <= 0:
        # opcional: pode permitir remover diretamente em vez de deixar 0.
        db.delete(item)
        db.commit()
        return None  # sinaliza que não existe mais

    unit = compute_unit_price(db, item.prato_id, item.bebida_id, item.extra_id)
    item.preco_unitario = unit
    item.subtotal = unit * Decimal(total_qty)

    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def remove_cart_item(db: Session, usuario_id: str | UUID, item_id: int):
    cart = get_open_cart_for_user(db, usuario_id)
    item = db.query(CarrinhoItem).filter(CarrinhoItem.id == item_id, CarrinhoItem.carrinho_id == cart.id).first()
    if not item:
        return None
    db.delete(item)
    db.commit()
    return True

def clear_cart(db: Session, usuario_id: str | UUID):
    cart = get_open_cart_for_user(db, usuario_id)
    items = db.query(CarrinhoItem).filter(CarrinhoItem.carrinho_id == cart.id).all()
    for it in items:
        db.delete(it)
    db.commit()
    return True

def get_cart_totals(db: Session, usuario_id: str | UUID):
    _, items = list_cart_items(db, usuario_id)
    total = sum([Decimal(str(it.subtotal)) for it in items])
    total_itens = sum([it.quantidade_prato + it.quantidade_bebida + it.quantidade_extra for it in items])
    return {"total": total, "total_itens": total_itens, "items_count": len(items)}
