from faker import Faker
import psycopg2
from psycopg2.extras import execute_batch
from psycopg2 import sql
import random
from datetime import datetime
import uuid
import time
import os
from dotenv import load_dotenv

load_dotenv()

fake = Faker('pt_BR')

TOTAL = 10000
BATCH_SIZE = 500

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_DATABASE")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


conn = psycopg2.connect(
    host=DB_HOST,
    database="postgres",
    user=DB_USER,
    password=DB_PASSWORD,
)

conn.autocommit = True
cursor = conn.cursor()

# Verifica se o banco existe
cursor.execute(
    "SELECT 1 FROM pg_database WHERE datname = %s",
    (DB_NAME,)
)

exists = cursor.fetchone()

if not exists:
    print(f"Criando banco '{DB_NAME}'...")

    cursor.execute(
        sql.SQL("CREATE DATABASE {}").format(
            sql.Identifier(DB_NAME)
        )
    )

    print(f"Banco '{DB_NAME}' criado com sucesso!")

else:
    print(f"Banco '{DB_NAME}' já existe.")

cursor.close()
conn.close()

# --------------------------------------------------
# CONECTA NO BANCO benchmarking
# --------------------------------------------------

conn = psycopg2.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
)

cursor = conn.cursor()

# --------------------------------------------------
# CRIA TABELA
# --------------------------------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id UUID PRIMARY KEY,
    nome TEXT,
    email TEXT,
    idade INT,
    cidade TEXT,
    salario DOUBLE PRECISION,
    created_at TIMESTAMP
)
""")

conn.commit()

# --------------------------------------------------
# INSERT EM MASSA
# --------------------------------------------------

start = time.time()

for batch_start in range(0, TOTAL, BATCH_SIZE):

    dados = []

    for _ in range(BATCH_SIZE):

        dados.append((
            str(uuid.uuid4()),
            fake.name(),
            fake.email(),
            random.randint(18, 80),
            fake.city(),
            round(random.uniform(1500, 20000), 2),
            datetime.now()
        ))

    execute_batch(cursor, """
        INSERT INTO usuarios (
            id,
            nome,
            email,
            idade,
            cidade,
            salario,
            created_at
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """, dados)

    conn.commit()

    print(f"{batch_start + BATCH_SIZE} registros inseridos")

end = time.time()

print(f"\nTempo total: {end - start:.2f} segundos")

cursor.close()
conn.close()