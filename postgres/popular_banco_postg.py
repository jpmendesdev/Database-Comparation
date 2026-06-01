from faker import Faker
import psycopg2
import random
from datetime import datetime
import uuid
import time
import os
from dotenv import load_dotenv

load_dotenv()

fake = Faker('pt_BR')

TOTAL = 100_000

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_DATABASE"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

cursor = conn.cursor()

inicio = time.time()

for i in range(TOTAL):

    cursor.execute("""
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
    """, (
        str(uuid.uuid4()),
        fake.name(),
        fake.email(),
        random.randint(18, 80),
        fake.city(),
        random.uniform(1500, 20000),
        datetime.now()
    ))

    if (i + 1) % 10000 == 0:
        print(f"{i+1:,} inseridos")

conn.commit()

fim = time.time()

print(f"INSERT DE 100.000 USUÁRIOS NO POSTGRES DEMOROU: {fim - inicio:.2f}s")

cursor.close()
conn.close()