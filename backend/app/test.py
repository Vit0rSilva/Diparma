from pydantic import ValidationError
from schemas.tipoBebidas import TipoBebidaBase

try:
    tipoBebida = TipoBebidaBase(
        tipo="23",  # se isso for inválido, Pydantic vai lançar erro
    )
    print("✅ Validação bem-sucedida!")
    print(tipoBebida.model_dump())
    print("Test passed")

except ValidationError as e:
    print("❌ Erro de validação:")
    print(e)
    print("Test failed")
