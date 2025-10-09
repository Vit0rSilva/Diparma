# app/services/auth_service.py
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from typing import Dict, Any
from fastapi import HTTPException, status

# Configuráveis (mova para settings/env)
SECRET_KEY = "substitua-por-uma-secret-real-e-complexa"  # trocar por variável de ambiente
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # exemplo: 24 horas (ajuste conforme necessidade)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(subject: str, expires_delta: int = None, extra_claims: Dict[str, Any] = None) -> Dict[str, Any]:
    now = datetime.utcnow()
    if expires_delta is None:
        expires_delta = ACCESS_TOKEN_EXPIRE_MINUTES * 60  # segundos
    expire = now + timedelta(seconds=expires_delta)
    payload = {
        "sub": subject,
        "iat": int(now.timestamp()),
        "exp": int(expire.timestamp()),
        "typ": "access"
    }
    if extra_claims:
        payload.update(extra_claims)
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "expires_in": expires_delta}
