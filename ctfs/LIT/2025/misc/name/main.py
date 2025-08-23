import multiprocessing as mp
import sys
import os
import time

def run_eval(code):
    sys.stdout = open(os.devnull, "w")
    sys.stderr = open(os.devnull, "w")
    try:
        eval(code)
    except Exception:
        pass

def eval_with_timeout(code, timeout_seconds=2):
    p = mp.Process(target=run_eval, args=(code,))
    p.start()
    p.join(timeout_seconds)
    if p.is_alive():
        p.terminate()
        p.join()

evalstring = input()
begin = time.time()
eval_with_timeout(evalstring, timeout_seconds=2)
while time.time() - begin < 5:
    pass
