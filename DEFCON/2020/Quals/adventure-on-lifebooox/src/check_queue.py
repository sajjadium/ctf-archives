import traceback
import redis
import rq

rq.use_connection(redis.Redis())
q = rq.Queue("lifeboxQueue")
print(q.count)
workers = rq.Worker.all(queue=q)
for w in workers:
    print(f"{w.name} - {w.get_state()} - {w.get_current_job()}")



