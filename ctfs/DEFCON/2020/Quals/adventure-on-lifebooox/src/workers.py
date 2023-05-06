
import multiprocessing
import traceback
import redis
import time
import sys
import rq
import os


def main():
    max_workers = 5
    if "GOL_WORKERS" in os.environ:
        max_workers = int(os.getenv("GOL_WORKERS"))

    processes = []
    q = None
    for _ in range(0, 3):
        try:
            rq.use_connection(redis.Redis())
            q = rq.Queue("lifeboxQueue")
            break
        except Exception:
            time.sleep(5)

    if q is None:
        print("Could not establish connection to redis, exiting")
        sys.exit(99)

    for _ in range(0, max_workers):
        try:
            proc = multiprocessing.Process(target=rq.Worker(q).work)
            proc.start()
            processes.append(proc)
        except Exception as ex:
            print(ex)
            traceback.print_exc()

    try:
        while True:
            tbd = []
            for proc in processes:
                if not proc.is_alive():
                    try:
                        tbd.append(proc)
                        newproc = multiprocessing.Process(target=rq.Worker(q).work)
                        newproc.start()
                        processes.append(newproc)
                    except Exception as ex:
                        print(ex)
                        traceback.print_exc()

            for proc in tbd:
                processes.remove(proc)

            time.sleep(10)

    except KeyboardInterrupt:
        print("interrupred, exiting and killing")
        pass
    finally:
        for proc in processes:
            proc.kill()



if __name__ == '__main__':
    main()



