# app/api/admins.py
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.administrador_shemas import AdministradorCreate, AdministradorOut, AdministradorLogin, Token
from app.repositories.administrador_repositories import AdministradorRepository
from app.deps import get_administrador_repo, get_current_administrador
from app.core.security import hash_password, verify_password
from app.core.jwt_handler import create_access_token
from app.service.authAdm import create_administrador_service
from fastapi.responses import JSONResponse
from app.schemas.response_schemas import SuccessResponse 

router = APIRouter(prefix="/admins", tags=["admins"])

@router.post("", response_model=SuccessResponse, status_code=status.HTTP_201_CREATED)
def create_administrador(
    payload: AdministradorCreate,
    repo: AdministradorRepository = Depends(get_administrador_repo)
):
    content = create_administrador_service(payload, repo)

    return SuccessResponse(
        message="Administrador criado com sucesso",
        data=content
    )


@router.post("/login", response_model=SuccessResponse)
def login(payload: AdministradorLogin, repo: AdministradorRepository = Depends(get_administrador_repo)):
    admin = repo.get_by_email(payload.email)
    if not admin or not verify_password(payload.senha, admin.senha):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={"message": "Email ou senha inválidos", "error_code": "EMAIL_SENHA_FALSE"}, headers={"WWW-Authenticate": "Bearer"})
    if not admin.ativo:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={"message": "Administrador Invalido", "error_code":"ADMIN_INATIVO"}, headers={"WWW-Authenticate": "Bearer"})

    token_data = create_access_token(subject=admin.id)
    return SuccessResponse(
        message="Login realizado com sucesso",
        data= {"access_token": token_data["access_token"], "token_type": "bearer", "expires_in": token_data["expires_in"]}
    )

@router.get("/me", response_model=SuccessResponse)
def me(current_admin = Depends(get_current_administrador)):
    data_admin = AdministradorOut.model_validate(current_admin).model_dump()
    return SuccessResponse(
        message="Administrador autenticado",
        data=data_admin
    )
