from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException

from app.database import Base, engine
from app.routers import tipoBebidas_routers, bebidas_routers, pratos_routers, tipoPrato_routers , admins_routers, usuarios_routers, endereco_routers, extra_routers, carrinho_routers, pedido_routers
from app.middlewares.error_handler import (
    http_exception_handler,
    validation_error_handler,
    generic_exception_handler,
)

app = FastAPI(title="Diparma API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registra handlers para EXCEÇÕES específicas (substitui o comportamento padrão)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_error_handler)
app.add_exception_handler(Exception, generic_exception_handler)  # opcional, para erros inesperados

# Cria as tabelas
Base.metadata.create_all(bind=engine)

# Registra rotas
app.include_router(admins_routers.router)
app.include_router(tipoBebidas_routers.router)
app.include_router(bebidas_routers.router)
app.include_router(tipoPrato_routers.router)
app.include_router(extra_routers.router)
app.include_router(pratos_routers.router)
app.include_router(usuarios_routers.router)
app.include_router(endereco_routers.router)
app.include_router(carrinho_routers.router)
app.include_router(pedido_routers.router)
