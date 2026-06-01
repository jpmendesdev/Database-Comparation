from cassandra.cluster import Cluster
from cassandra import ConsistencyLevel
from faker import Faker
import uuid
import random
from datetime import datetime
import time

fake = Faker('pt_BR')

TOTAL = 100_000

cluster = Cluster(['127.0.0.1'])
session = cluster.connect('benchmark')

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

prepared.consistency_level = ConsistencyLevel.ONE

inicio = time.time()

for i in range(TOTAL):

    session.execute(
        prepared,
        (
            uuid.uuid4(),
            fake.name(),
            fake.email(),
            random.randint(18, 80),
            fake.city(),
            random.uniform(1500, 20000),
            datetime.now()
        )
    )

    if (i + 1) % 10000 == 0:
        print(f"{i+1:,} inseridos")

fim = time.time()

print(f"\nINSERT DE 100.000 USUÁRIOS NO CASSANDRA DEMOROU: {fim - inicio:.2f}s")

cluster.shutdown()