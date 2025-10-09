import jwt
from uuid import UUID
from app.core.jwt_handler import SECRET_KEY, ALGORITHM
from app.repositories.administrador_repositories import AdministradorRepository
from app.database import SessionLocal

# Copie aqui exatamente a mesma chave usada na geração do token
SECRET_KEY = "troque_por_alguma_secret_na_producao"
ALGORITHM = "HS256"

# Cole aqui o token JWT retornado pelo login
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMDEzZjNlOC02OWNhLTQ4YWUtYjkzYi01ZThhYzg2ZmY3NjQiLCJpYXQiOjE3NjAwMzc5MzEsImV4cCI6MTc2MDEyNDMzMSwidHlwIjoiYWNjZXNzIn0.prdzwCiNBdeHETHFBdli1TGTD_kcrZn8wdB0hk18sDU"

# Cria sessão do banco
db = SessionLocal()
repo = AdministradorRepository(db)

try:
    # Decodifica o token com leeway de 10 segundos
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], leeway=10)
    print("Payload decodificado:", payload)

    # Converte sub para UUID
    admin_id = UUID(payload.get("sub"))
    admin = repo.get_by_id(admin_id)

    if not admin:
        print("Admin não encontrado no banco")
    elif not admin.ativo:
        print("Admin inativo")
    else:
        print("Admin autenticado com sucesso:", admin.email)

except jwt.ExpiredSignatureError:
    print("Token expirado")
except jwt.ImmatureSignatureError:
    print("Token ainda não é válido (iat)")
except jwt.InvalidTokenError:
    print("Token inválido")

finally:
    db.close()
