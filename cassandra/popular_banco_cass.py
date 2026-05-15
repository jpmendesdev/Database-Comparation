from cassandra.cluster import Cluster
from cassandra.query import BatchStatement
from faker import Faker
import uuid
import random
from datetime import datetime
import time

'''
ANTES DE RODAR ESSE SCRIPT VOCÊ DEVE TER CRIADO UM CONTAINER E SUBIDO O CASSANDRA, SE NÃO FEZ ESSE É O COMANDO:

    docker run --name cassandra \
    -p 9042:9042 \
    -d cassandra:latest
    
AGUARDA UM POUCO E DEPOIS RODA O SCRIPT


ATENÇÃO!!! ESSE SCRIPT CRIA E INSERE 1.000.000 DE USUÁRIOS NO BANCO, ENTÃO POR DEUS DO CÉU, RODE APENAS UMA VEZ
'''

fake = Faker('pt_BR')

TOTAL = 10000
BATCH_SIZE = 50

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

for batch_start in range(0, TOTAL, BATCH_SIZE):

    batch = BatchStatement()

    for _ in range(BATCH_SIZE):

        batch.add(prepared, (
            uuid.uuid4(),
            fake.name(),
            fake.email(),
            random.randint(18, 80),
            fake.city(),
            round(random.uniform(1500, 20000), 2),
            datetime.now()
        ))

    session.execute(batch)

    print(f"{batch_start + BATCH_SIZE} registros inseridos")

end = time.time()

print(f"Tempo total: {end - start:.2f} segundos")