import time
from cassandra.cluster import Cluster

cluster = Cluster(['127.0.0.1'], port=9042)
session = cluster.connect("benchmark")

# pega um id real de teste (IMPORTANTE)
row = session.execute("""
SELECT id FROM usuarios_por_grupo WHERE grupo='A' LIMIT 1
""").one()

test_id = row.id

start = time.time()

result = session.execute("""
SELECT *
FROM usuarios_por_grupo
WHERE grupo='A' AND id=%s
""", (test_id,))

data = list(result)

end = time.time()

print("Cassandra")
print(len(data))
print(end - start)

cluster.shutdown()