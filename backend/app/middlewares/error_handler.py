from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.schemas.response_schemas import ErrorResponse

# ⚙️ Middleware principal para erros de execução
async def error_handler(request: Request, call_next):
    try:
        return await call_next(request)

    except IntegrityError as exc:
        # Captura mensagem original do banco (útil para depuração)
        error_message = str(exc.orig).lower()

        # Detecta erro de duplicidade
        if "unique constraint" in error_message or "duplicate" in error_message:
            mensagem = "Já existe um registro com esse valor."
            error_code = "DUPLICATE_ENTRY"
        else:
            mensagem = "Erro de integridade no banco de dados."
            error_code = "INTEGRITY_ERROR"

        return JSONResponse(
            status_code=400,
            content=ErrorResponse(
                error_code=error_code,
                message=mensagem
            ).model_dump(),
        )

    except HTTPException as exc:
        # Verifica se o detail já vem como dict (nos nossos erros customizados)
        if isinstance(exc.detail, dict):
            content = ErrorResponse(
                success=False,
                error_code=exc.detail.get("error_code"),
                message=exc.detail.get("message")
            ).model_dump()
        else:
            content = ErrorResponse(message=str(exc.detail)).model_dump()

        return JSONResponse(status_code=exc.status_code, content=content)

    except IntegrityError:
        return JSONResponse(
            status_code=400,
            content=ErrorResponse(
                error_code="INTEGRITY_ERROR",
                message="Erro de integridade no banco de dados (valor duplicado ou inválido)."
            ).model_dump(),
        )

    except SQLAlchemyError:
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(
                error_code="DATABASE_ERROR",
                message="Erro interno no banco de dados."
            ).model_dump(),
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content=ErrorResponse(
                error_code="UNEXPECTED_ERROR",
                message=f"Erro inesperado: {str(e)}"
            ).model_dump(),
        )


# ⚙️ Captura erros de validação Pydantic
async def validation_error_handler(request: Request, exc: RequestValidationError):
    erros = []
    for err in exc.errors():
        erros.append({
            "campo": " → ".join(map(str, err["loc"])),
            "mensagem": err["msg"],
            "tipo": err["type"],
            "valor_enviado": err.get("input")
        })

    return JSONResponse(
        status_code=422,
        content=ErrorResponse(
            error_code="VALIDATION_ERROR",
            message="Erro de validação nos dados enviados.",
            data={"erros": erros}
        ).model_dump(),
    )
