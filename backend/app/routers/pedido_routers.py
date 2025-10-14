# app/api/pedidos.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import pedido_schemas, response_schemas
from app.repositories import pedido_repositories as pedido_repo
from app.deps import get_db, get_current_usuario

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

@router.post("/", response_model=response_schemas.SuccessResponse)
def criar_pedido(payload: pedido_schemas.PedidoCreate, db: Session = Depends(get_db), usuario=Depends(get_current_usuario)):
    """
    Cria um pedido a partir do carrinho do usuário.
    """
    pedido, err = pedido_repo.create_pedido_from_cart(db, usuario.id, payload)
    if err:
        raise HTTPException(status_code=400, detail=err)

    # Converte o pedido e itens para o modelo Pydantic
    pedido_response = pedido_schemas.PedidoResponse(
        id=str(pedido.id),
        usuario_id=str(pedido.usuario_id),
        status=pedido.status,
        total=pedido.total,
        id_endereco=pedido.id_endereco,
        frete=pedido.frete,
        retirada_boll=pedido.retirada_boll,
        horario_retirada=pedido.horario_retirada,
        observacao=pedido.observacao,
        itens=[
            pedido_schemas.PedidoItemResponse(
                id=item.id,
                nome=item.nome,
                quantidade=item.quantidade,
                preco_unitario=item.preco_unitario,
                subtotal=item.subtotal
            )
            for item in pedido.itens
        ],
        criado_em=pedido.criado_em,
        atualizado_em=pedido.atualizado_em
    )

    return response_schemas.SuccessResponse(message="Pedido criado com sucesso", data=pedido_response)


@router.get("/", response_model=response_schemas.SuccessResponse)
def listar_pedidos(db: Session = Depends(get_db), usuario=Depends(get_current_usuario)):
    """
    Lista todos os pedidos do usuário.
    """
    pedidos = pedido_repo.get_pedidos_by_user(db, usuario.id)

    data = []
    for p in pedidos:
        pedido_response = pedido_schemas.PedidoResponse(
            id=str(p.id),
            usuario_id=str(p.usuario_id),
            status=p.status,
            total=p.total,
            id_endereco=p.id_endereco,
            frete=p.frete,
            retirada_boll=p.retirada_boll,
            horario_retirada=p.horario_retirada,
            observacao=p.observacao,
            itens=[
                pedido_schemas.PedidoItemResponse(
                    id=item.id,
                    nome=item.nome,
                    quantidade=item.quantidade,
                    preco_unitario=item.preco_unitario,
                    subtotal=item.subtotal
                )
                for item in p.itens
            ],
            criado_em=p.criado_em,
            atualizado_em=p.atualizado_em
        )
        data.append(pedido_response)

    return response_schemas.SuccessResponse(message="Pedidos do usuário", data=data)


@router.get("/{pedido_id}", response_model=response_schemas.SuccessResponse)
def pedido_por_id(pedido_id: str, db: Session = Depends(get_db), usuario=Depends(get_current_usuario)):
    """
    Retorna um pedido específico do usuário.
    """
    pedido = pedido_repo.get_pedido(db, pedido_id, usuario.id)
    if not pedido:
        raise HTTPException(status_code=404, detail={"message": "Pedido não encontrado", "error_code": "NOT_FOUND_PEDIDO"})

    pedido_response = pedido_schemas.PedidoResponse(
        id=str(pedido.id),
        usuario_id=str(pedido.usuario_id),
        status=pedido.status,
        total=pedido.total,
        id_endereco=pedido.id_endereco,
        frete=pedido.frete,
        retirada_boll=pedido.retirada_boll,
        horario_retirada=pedido.horario_retirada,
        observacao=pedido.observacao,
        itens=[
            pedido_schemas.PedidoItemResponse(
                id=item.id,
                nome=item.nome,
                quantidade=item.quantidade,
                preco_unitario=item.preco_unitario,
                subtotal=item.subtotal
            )
            for item in pedido.itens
        ],
        criado_em=pedido.criado_em,
        atualizado_em=pedido.atualizado_em
    )

    return response_schemas.SuccessResponse(message="Pedido encontrado", data=pedido_response)
