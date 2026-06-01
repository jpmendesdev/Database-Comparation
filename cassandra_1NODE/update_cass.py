import time
import random

from cassandra.cluster import Cluster
from cassandra import ConsistencyLevel
from cassandra.query import SimpleStatement

TOTAL_UPDATES = 10000
TOTAL_IDS_CARREGADOS = 100000
MAX_IN_FLIGHT = 500

cluster = Cluster(['127.0.0.1'])
session = cluster.connect()
session.set_keyspace('benchmark')

statement = SimpleStatement(
    f"SELECT id FROM usuarios LIMIT {TOTAL_IDS_CARREGADOS}",
    fetch_size=5000
)

rows = session.execute(statement)

ids = [row.id for row in rows]

print(f"IDs carregados: {len(ids)}")

amostra = random.sample(ids, TOTAL_UPDATES)

prepared = session.prepare(
    """
    UPDATE usuarios
    SET salario = ?
    WHERE id = ?
    """
)

prepared.consistency_level = ConsistencyLevel.ONE


start = time.time()

futures = []

for user_id in amostra:

    novo_salario = round(
        random.uniform(1500, 20000),
        2
    )

    futures.append(
        session.execute_async(
            prepared,
            [novo_salario, user_id]
        )
    )

    if len(futures) >= MAX_IN_FLIGHT:

        for future in futures:
            future.result()

        futures.clear()

for future in futures:
    future.result()

end = time.time()

tempo = end - start

print("\n=== RESULTADO ===")
print(f"Tempo total: {tempo:.2f}s")

cluster.shutdown()