import psycopg2
import uuid
import time
import os
from dotenv import load_dotenv

load_dotenv()

TOTAL = 1_000_000

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_DATABASE")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

conn = psycopg2.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)

cur = conn.cursor()

inicio = time.time()

for i in range(TOTAL):

    cur.execute("""
        INSERT INTO usuarios(
            id,
            nome,
            email,
            idade,
            cidade,
            salario,
            created_at
        )
        VALUES(
            %s,%s,%s,%s,%s,%s,NOW()
        )
    """, (
        str(uuid.uuid4()),
        "Teste",
        "teste@email.com",
        30,
        "Fortaleza",
        5000.0
    ))

conn.commit()

fim = time.time()

print(f"Tempo: {fim-inicio:.2f}s")