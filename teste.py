import time
import uuid
import random
from datetime import datetime

import psycopg2
from psycopg2.extras import execute_values
from faker import Faker
from dotenv import load_dotenv
import os

load_dotenv()

fake = Faker('pt_BR')

DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_DATABASE")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

TOTAL = 1_000_000
BATCH_SIZE = 5000

conn = psycopg2.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)

cursor = conn.cursor()

start = time.time()

for inicio in range(0, TOTAL, BATCH_SIZE):

    registros = []

    for _ in range(BATCH_SIZE):

        registros.append(
            (
                str(uuid.uuid4()),
                fake.name(),
                fake.email(),
                random.randint(18, 80),
                fake.city(),
                round(random.uniform(1500, 20000), 2),
                datetime.now(),
                random.choice(['A', 'B', 'C', 'D', 'E'])
            )
        )

    execute_values(
        cursor,
        """
        INSERT INTO usuarios (
            id,
            nome,
            email,
            idade,
            cidade,
            salario,
            created_at,
            grupo
        )
        VALUES %s
        """,
        registros
    )

    conn.commit()

    inseridos = min(inicio + BATCH_SIZE, TOTAL)

    print(
        f"{inseridos:,}/{TOTAL:,} "
        f"({inseridos/(time.time()-start):.0f} inserts/s)"
    )

end = time.time()

print("\n=== RESULTADO ===")
print(f"Tempo: {end-start:.2f}s")
print(f"Throughput: {TOTAL/(end-start):.2f} inserts/s")

cursor.close()
conn.close()