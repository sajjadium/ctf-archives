#!/bin/sh

set -e

cd /home/ctf/

# First create admin user
python3 ./preregister_admin.py

cd /home/ctf/asmbb-challenge
nohup ./server &
/proxy 8091 8090

exit 0

