# test_connection.py
from app.database import get_connection

try:
    conn = get_connection()
    print("✅ Conexão bem-sucedida com o banco de dados!")
    conn.close()
except Exception as e:
    print("❌ Erro ao conectar:", e)
