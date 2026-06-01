import time
import random

from cassandra.cluster import Cluster
from cassandra import ConsistencyLevel
from cassandra.query import SimpleStatement

TOTAL_DELETES = 10000
TOTAL_IDS_CARREGADOS = 100000
MAX_IN_FLIGHT = 500

cluster = Cluster(['127.0.0.1'])
session = cluster.connect('benchmark')

statement = SimpleStatement(
    f"SELECT id FROM usuarios LIMIT {TOTAL_IDS_CARREGADOS}",
    fetch_size=5000
)

rows = session.execute(statement)
ids = [row.id for row in rows]

amostra = random.sample(ids, TOTAL_DELETES)

prepared = session.prepare(
    "DELETE FROM usuarios WHERE id = ?"
)

prepared.consistency_level = ConsistencyLevel.ONE

start = time.time()

futures = []

for user_id in amostra:

    futures.append(
        session.execute_async(
            prepared,
            [user_id]
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

print(f"DELETE Cassandra demorou: {tempo:.2f}s")

cluster.shutdown()