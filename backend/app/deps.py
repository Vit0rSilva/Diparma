from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.repositories.administrador_repositories import AdministradorRepository
from app.repositories.usuario_repositories import UsuarioRepository
import jwt
import os
from uuid import UUID

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/admins/login")
oauth2_usuario_scheme = OAuth2PasswordBearer(tokenUrl="/usuarios/login")

SECRET_KEY = os.getenv("SECRET_KEY", "troque_por_alguma_secret_na_producao")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_administrador_repo(db: Session = Depends(get_db)) -> AdministradorRepository:
    return AdministradorRepository(db)

def get_current_administrador(token: str = Depends(oauth2_scheme), repo: AdministradorRepository = Depends(get_administrador_repo)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não autenticado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # se quiser manter tolerância de iat/exp use leeway (em segundos)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], leeway=10)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expirado", headers={"WWW-Authenticate": "Bearer"})
    except jwt.ImmatureSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token ainda não válido (iat)", headers={"WWW-Authenticate": "Bearer"})
    except jwt.PyJWTError:
        raise credentials_exception

    sub = payload.get("sub")
    if sub is None:
        raise credentials_exception

    # Normaliza o sub para string canônica do UUID (com hífens) antes de consultar
    try:
        sub_str = str(UUID(str(sub)))
    except (ValueError, TypeError):
        raise credentials_exception

    admin = repo.get_by_id(sub_str)
    if admin is None or not admin.ativo:
        raise credentials_exception

    return admin


#Usuario
def get_usuario_repo(db: Session = Depends(get_db)) -> UsuarioRepository:
    return UsuarioRepository(db)

def get_current_usuario(token: str = Depends(oauth2_usuario_scheme), repo: UsuarioRepository = Depends(get_usuario_repo)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não autenticado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], leeway=10)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expirado", headers={"WWW-Authenticate": "Bearer"})
    except jwt.ImmatureSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token ainda não válido (iat)", headers={"WWW-Authenticate": "Bearer"})
    except jwt.PyJWTError:
        raise credentials_exception

    sub = payload.get("sub")
    if sub is None:
        raise credentials_exception

    try:
        sub_str = str(UUID(str(sub)))
    except (ValueError, TypeError):
        raise credentials_exception

    user = repo.get_by_id(sub_str)
    if user is None:
        raise credentials_exception

    return user
