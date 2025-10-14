# app/repositories/pedido_repositories.py
from sqlalchemy.orm import Session, joinedload
from app.models.pedido_models import Pedido, PedidoItem
from app.models.carrinho_models import Carrinho, CarrinhoItem
from app.models.endereco_models import Enderecos
from app.schemas.pedido_schemas import PedidoCreate
from uuid import UUID
from decimal import Decimal

def create_pedido_from_cart(db: Session, usuario_id: str, payload):
    # encontra carrinho aberto
    cart = db.query(Carrinho).filter(
        Carrinho.id == payload.carrinho_id,
        Carrinho.usuario_id == usuario_id,
        Carrinho.status == "aberto"
    ).first()

    if not cart:
        return None, {"message": "Carrinho não encontrado ou já fechado", "error_code": "CART_NOT_FOUND"}

    items = db.query(CarrinhoItem).options(
        joinedload(CarrinhoItem.prato),
        joinedload(CarrinhoItem.bebida),
        joinedload(CarrinhoItem.extra)
    ).filter(CarrinhoItem.carrinho_id == cart.id).all()

    if not items:
        return None, {"message": "Carrinho vazio", "error_code": "CART_EMPTY"}

    # 🔹 pega endereço principal do usuário
    endereco_principal = db.query(Enderecos).filter(
        Enderecos.usuario_id == usuario_id,
        Enderecos.endereco_principal == True
    ).first()

    if not endereco_principal:
        return None, {"message": "Usuário não possui endereço principal cadastrado", "error_code": "NO_MAIN_ADDRESS"}

    # 🔹 calcula total e cria pedido
    total = sum([Decimal(str(it.subtotal)) for it in items])

    pedido = Pedido(
        usuario_id=usuario_id,
        carrinho_id=cart.id,
        total=total,
        status="em_andamento",
        id_endereco=endereco_principal.id,
        frete=payload.frete,
        retirada_boll=payload.retirada_boll,
        horario_retirada=payload.horario_retirada,
        observacao=payload.observacao
    )

    db.add(pedido)
    db.commit()
    db.refresh(pedido)

    # adiciona itens do carrinho
    for it in items:
        parts = []
        if it.prato:
            parts.append(it.prato.nome)
        if it.bebida:
            parts.append(it.bebida.nome)
        if it.extra:
            parts.append(it.extra.nome)
        nome = " + ".join(parts) if parts else "Item"

        quantidade = it.quantidade_prato + it.quantidade_bebida + it.quantidade_extra
        pedido_item = PedidoItem(
            pedido_id=pedido.id,
            nome=nome,
            quantidade=quantidade,
            preco_unitario=it.preco_unitario,
            subtotal=it.subtotal
        )
        db.add(pedido_item)

    cart.status = "fechado"
    db.commit()
    db.refresh(pedido)

    return pedido, None


def get_pedidos_by_user(db: Session, usuario_id: str | UUID):
    return db.query(Pedido).filter(Pedido.usuario_id == str(usuario_id)).all()


def get_pedido(db: Session, pedido_id: str | UUID, usuario_id: str | UUID):
    return db.query(Pedido).filter(
        Pedido.id == str(pedido_id), Pedido.usuario_id == str(usuario_id)
    ).first()
