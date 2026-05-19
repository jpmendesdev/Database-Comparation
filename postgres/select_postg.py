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

conn = psycopg2.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
)

conn.autocommit = True
cursor = conn.cursor()

cursor.execute("SELECT id FROM usuarios")
ids = [row[0] for row in cursor.fetchall()]

start = time.time()


'''READ POSTGRES 10.000 USERS, DEMOROU 0.83s'''
for _ in range(10000):

    user_id = random.choice(ids)

    cursor.execute(
        "SELECT * FROM usuarios WHERE id = %s",
        (user_id,)
    )

    cursor.fetchone()

end = time.time()

print(f"READ PostgreSQL demorou: {end - start:.2f}s")