import time
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_DATABASE"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
)

cursor = conn.cursor()

start = time.time()

cursor.execute(
    """
    SELECT COUNT(*)
    FROM usuarios
    """
)

total = cursor.fetchone()[0]

end = time.time()

print("\n=== RESULTADO ===")
print(f"Total de registros: {total}")
print(f"Tempo: {end - start:.2f}s")

cursor.close()
conn.close()