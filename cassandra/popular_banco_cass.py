from cassandra.cluster import Cluster
from faker import Faker
import uuid
import random
from datetime import datetime
import time

fake = Faker('pt_BR')

TOTAL = 10000000
MAX_IN_FLIGHT = 1000

cluster = Cluster(['127.0.0.1'])
session = cluster.connect()

session.execute("""
CREATE KEYSPACE IF NOT EXISTS benchmark
WITH replication = {
    'class': 'SimpleStrategy',
    'replication_factor': 1
}
""")

session.set_keyspace('benchmark')

session.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id UUID PRIMARY KEY,
    nome TEXT,
    email TEXT,
    idade INT,
    cidade TEXT,
    salario DOUBLE,
    created_at TIMESTAMP
)
""")

prepared = session.prepare("""
INSERT INTO usuarios (
    id,
    nome,
    email,
    idade,
    cidade,
    salario,
    created_at
)
VALUES (?, ?, ?, ?, ?, ?, ?)
""")

start = time.time()

futures = []
inseridos = 0

for _ in range(TOTAL):

    future = session.execute_async(
        prepared,
        (
            uuid.uuid4(),
            fake.name(),
            fake.email(),
            random.randint(18, 80),
            fake.city(),
            round(random.uniform(1500, 20000), 2),
            datetime.now()
        )
    )

    futures.append(future)
    inseridos += 1

    if len(futures) >= MAX_IN_FLIGHT:
        for f in futures:
            f.result()

        futures.clear()

        print(f"{inseridos} registros inseridos")

for f in futures:
    f.result()

end = time.time()

print(f"\nTempo total: {end - start:.2f} segundos")

cluster.shutdown()

#DEMOROU 209 SEGUNDOS PARA INSERIR 1.000.000 usuários
#DEMOROU 2067 SEGUNDOS PARA INSERIR 1.000.000 usuários
#DELETE demorou 3 segundos