# app/api/usuarios.py
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.usuario_schemas import UsuarioCreate, UsuarioOut, UsuarioLogin
from app.repositories.usuario_repositories import UsuarioRepository
from app.deps import get_usuario_repo, get_current_usuario, get_db
from app.core.security import verify_password
from app.core.jwt_handler import create_access_token
from app.service.authUsuario import create_usuario_service
from app.schemas.response_schemas import SuccessResponse
from sqlalchemy.orm import Session
from app.repositories import endereco_repositories
from app.schemas import endereco_schemas


router = APIRouter(prefix="/usuarios", tags=["usuarios"])

@router.post("", response_model=SuccessResponse, status_code=status.HTTP_201_CREATED)
def create_usuario(
    payload: UsuarioCreate,
    repo: UsuarioRepository = Depends(get_usuario_repo)
):
    content = create_usuario_service(payload, repo)
    return SuccessResponse(message="Usuário criado com sucesso", data=content)

@router.post("/login", response_model=SuccessResponse)
def login(payload: UsuarioLogin, repo: UsuarioRepository = Depends(get_usuario_repo)):
    usuario = repo.get_by_email(payload.email)
    if not usuario or not verify_password(payload.senha, usuario.senha):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"message": "Email ou senha inválidos", "error_code": "EMAIL_SENHA_FALSE"}, headers={"WWW-Authenticate": "Bearer"})
    token_data = create_access_token(subject=usuario.id)
    return SuccessResponse(message="Login realizado com sucesso", data={"access_token": token_data["access_token"], "token_type": "bearer", "expires_in": token_data["expires_in"]})

@router.get("/me", response_model=SuccessResponse)
def me(current_user = Depends(get_current_usuario)):
    data_user = UsuarioOut.model_validate(current_user).model_dump()
    return SuccessResponse(message="Usuário autenticado", data=data_user)

@router.get("/me/enderecos", response_model=SuccessResponse)
def listar_enderecos_usuario(
    db: Session = Depends(get_db),
    usuario = Depends(get_current_usuario)
):
    enderecos = endereco_repositories.get_enderecos_by_usuario(db, usuario.id)
    enderecos_data = [
        endereco_schemas.EnderecoResponse.model_validate(e).model_dump()
        for e in enderecos
    ]

    return SuccessResponse(
        message="Listando endereços do usuário autenticado.",
        data=enderecos_data
    )