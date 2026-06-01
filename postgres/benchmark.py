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

cur = conn.cursor()

# pega um id real
cur.execute("""
SELECT id FROM usuarios_por_grupo WHERE grupo='A' LIMIT 1
""")

test_id = cur.fetchone()[0]

start = time.time()

cur.execute("""
SELECT *
FROM usuarios_por_grupo
WHERE grupo='A' AND id=%s
""", (test_id,))

data = cur.fetchall()

end = time.time()

print("PostgreSQL")
print(len(data))
print(end - start)

cur.close()
conn.close()