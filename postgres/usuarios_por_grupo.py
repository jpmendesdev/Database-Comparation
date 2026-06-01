import time
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_DATABASE"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

cursor = conn.cursor()

print("Limpando tabela...")

cursor.execute("""
TRUNCATE TABLE usuarios_por_grupo;
""")

conn.commit()

print("Iniciando carga...")

inicio = time.time()

cursor.execute("""
INSERT INTO usuarios_por_grupo
SELECT
    CASE floor(random() * 5)
        WHEN 0 THEN 'A'
        WHEN 1 THEN 'B'
        WHEN 2 THEN 'C'
        WHEN 3 THEN 'D'
        ELSE 'E'
    END AS grupo,
    id,
    nome,
    email,
    idade,
    cidade,
    salario,
    created_at
FROM usuarios;
""")

conn.commit()

fim = time.time()

print("\n=== RESULTADO ===")
print(f"Tempo carga: {fim - inicio:.2f}s")

cursor.close()
conn.close()