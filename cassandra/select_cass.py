import time
import random
from cassandra.cluster import Cluster


cluster = Cluster(['127.0.0.1'])
session = cluster.connect()
session.set_keyspace('benchmark')


rows = session.execute("SELECT id FROM usuarios")
ids = [row.id for row in rows]

prepared = session.prepare(
    "SELECT * FROM usuarios WHERE id = ?"
)

start = time.time()


'''READ CASSANDRA 10.000 USERS, DEMOROU 20s'''
for _ in range(10000):

    user_id = random.choice(ids)

    session.execute(prepared, [user_id]).one()

end = time.time()

print(f"READ Cassandra demorou: {end - start:.2f}s")