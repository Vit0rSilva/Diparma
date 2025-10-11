from fastapi import HTTPException, status
from app.schemas.administrador_shemas import AdministradorCreate, AdministradorOut
from app.core.security import hash_password
from app.core.jwt_handler import create_access_token
from app.repositories.administrador_repositories import AdministradorRepository

def create_administrador_service(payload: AdministradorCreate, repo: AdministradorRepository):
    if repo.get_by_email(payload.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Email já cadastrado", "error_code": "EMAIL_EXISTS"}
        )


    if repo.get_by_cpf(payload.cpf):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "CPF já cadastrado", "error_code": "CPF_EXISTS"}
        )

    hashed = hash_password(payload.senha)

    admin = repo.create(payload, hashed_password=hashed)

    token_data = create_access_token(subject=admin.id)

    out = AdministradorOut.model_validate(admin)

    return {
        **out.model_dump(mode="json"),
        "access_token": token_data["access_token"],
        "expires_in": token_data["expires_in"]
    }
