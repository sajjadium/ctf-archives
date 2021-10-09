#!/bin/bash

ulimit -t 5
ulimit -u 1000

cd /app

timeout -s KILL 300 "$@"
