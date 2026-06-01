import time
import random

from cassandra.cluster import Cluster
from cassandra import ConsistencyLevel
from cassandra.query import SimpleStatement

# Configurações
TOTAL_READS = 10000
TOTAL_IDS_CARREGADOS = 100000
MAX_IN_FLIGHT = 500

# Conexão
cluster = Cluster(['127.0.0.1'])
session = cluster.connect()
session.set_keyspace('benchmark')

inicio_ids = time.time()

# Carrega apenas uma amostra dos IDs da tabela
statement = SimpleStatement(
    f"SELECT id FROM usuarios LIMIT {TOTAL_IDS_CARREGADOS}",
    fetch_size=5000
)

rows = session.execute(statement)
ids = [row.id for row in rows]

fim_ids = time.time()


if len(ids) < TOTAL_READS:
    raise Exception(
        f"Apenas {len(ids)} IDs foram carregados. "
        f"Necessário pelo menos {TOTAL_READS}."
    )

# Seleciona 10.000 IDs aleatórios
amostra = random.sample(ids, TOTAL_READS)

prepared = session.prepare(
    "SELECT * FROM usuarios WHERE id = ?"
)

prepared.consistency_level = ConsistencyLevel.ONE


inicio_reads = time.time()

futures = []

for user_id in amostra:

    futures.append(
        session.execute_async(
            prepared,
            [user_id]
        )
    )

    # Limita a quantidade de consultas simultâneas
    if len(futures) >= MAX_IN_FLIGHT:

        for future in futures:
            future.result().one()

        futures.clear()

# Processa o restante
for future in futures:
    future.result().one()

fim_reads = time.time()

tempo_reads = fim_reads - inicio_reads

print("\n=== RESULTADO ===")
print(f"Leituras realizadas: {TOTAL_READS}")
print(f"Tempo total de leitura: {tempo_reads:.2f}s")

cluster.shutdown()