#!/bin/sh

ulimit -m 4096 && exec socat -T 5 TCP-LISTEN:55555,reuseaddr,fork,su=treasure EXEC:"python prob.py",stderr
