from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.database import Base, engine
from app.routers import tipoBebidas_routers, admins_routers
from app.middlewares.error_handler import error_handler
from app.middlewares.error_handler import validation_error_handler
from fastapi.exceptions import RequestValidationError


app = FastAPI(title="Diparma API")

# ⚙️ Permitir que o Angular acesse o backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # origem do Angular
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware("http")(error_handler)

# ⚙️ Registra o tratador específico para erros de validação Pydantic
app.add_exception_handler(RequestValidationError, validation_error_handler)

# Cria as tabelas
Base.metadata.create_all(bind=engine)

# Registra rotas
app.include_router(tipoBebidas_routers.router)
app.include_router(admins_routers.router)
