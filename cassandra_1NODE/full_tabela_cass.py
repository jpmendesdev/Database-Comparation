import time

from cassandra.cluster import Cluster

cluster = Cluster(['127.0.0.1'])

session = cluster.connect()
session.set_keyspace('benchmark')

start = time.time()

resultado = session.execute(
    """
    SELECT COUNT(*)
    FROM usuarios
    """
)

total = resultado.one().count

end = time.time()

print("\n=== RESULTADO ===")
print(f"Total de registros: {total}")
print(f"Tempo: {end - start:.2f}s")

cluster.shutdown()