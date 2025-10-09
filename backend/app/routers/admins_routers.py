# app/api/admins.py
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.administrador_shemas import AdministradorCreate, AdministradorOut, AdministradorLogin, Token
from app.repositories.administrador_repositories import AdministradorRepository
from app.deps import get_administrador_repo, get_current_administrador
from app.core.security import hash_password, verify_password
from app.core.jwt_handler import create_access_token
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/admins", tags=["admins"])

@router.post("", response_model=AdministradorOut, status_code=status.HTTP_201_CREATED)
def create_administrador(payload: AdministradorCreate, repo: AdministradorRepository = Depends(get_administrador_repo)):
    if repo.get_by_email(payload.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email já cadastrado")
    if repo.get_by_cpf(payload.cpf):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="CPF já cadastrado")

    hashed = hash_password(payload.senha)
    admin = repo.create(payload, hashed_password=hashed)
    # gerar token opcionalmente na criação
    token_data = create_access_token(subject=admin.id)
    out = AdministradorOut.model_validate(admin)  # pydantic v2
    # retornamos o admin + token se desejar
    # dentro da rota create_administrador
    content = out.model_dump(mode="json")
    content.update({"access_token": token_data["access_token"], "expires_in": token_data["expires_in"]})
    return JSONResponse(status_code=201, content=content)


@router.post("/login", response_model=Token)
def login(payload: AdministradorLogin, repo: AdministradorRepository = Depends(get_administrador_repo)):
    admin = repo.get_by_email(payload.email)
    if not admin or not verify_password(payload.senha, admin.senha):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email ou senha inválidos", headers={"WWW-Authenticate": "Bearer"})
    if not admin.ativo:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Administrador inativo")

    token_data = create_access_token(subject=admin.id)
    return {"access_token": token_data["access_token"], "token_type": "bearer", "expires_in": token_data["expires_in"]}

@router.get("/me", response_model=AdministradorOut)
def me(current_admin = Depends(get_current_administrador)):
    return AdministradorOut.model_validate(current_admin)
