from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# ⚙️ Permitir que o Angular acesse o backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # origem do Angular
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo de usuário
class Usuario(BaseModel):
    nome: str
    email: str

# Rotas
@app.get("/")
def home():
    return {"mensagem": "API FastAPI funcionando!"}

@app.post("/usuarios/")
def criar_usuario(usuario: Usuario):
    return {"mensagem": f"Usuário {usuario.nome} cadastrado com sucesso!"}
