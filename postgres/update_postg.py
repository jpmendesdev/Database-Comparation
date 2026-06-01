import time
import random
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_DATABASE")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

TOTAL_UPDATES = 10000
TOTAL_IDS_CARREGADOS = 100000

conn = psycopg2.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
)

cursor = conn.cursor()


cursor.execute(
    f"""
    SELECT id
    FROM usuarios
    LIMIT {TOTAL_IDS_CARREGADOS}
    """
)

ids = [row[0] for row in cursor.fetchall()]

print(f"IDs carregados: {len(ids)}")

amostra = random.sample(ids, TOTAL_UPDATES)

print(f"Iniciando benchmark de {TOTAL_UPDATES} updates...")

start = time.time()

for user_id in amostra:

    novo_salario = round(
        random.uniform(1500, 20000),
        2
    )

    cursor.execute(
        """
        UPDATE usuarios
        SET salario = %s
        WHERE id = %s
        """,
        (novo_salario, user_id)
    )

conn.commit()

end = time.time()

tempo = end - start

print("\n=== RESULTADO ===")
print(f"Tempo total: {tempo:.2f}s")

cursor.close()
conn.close()