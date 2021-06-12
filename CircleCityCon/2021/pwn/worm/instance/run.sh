#!/bin/bash

set -eu
./pre_build.sh $MAX_DEPTH
python3 -u build.py
rm -rf /keys key.c build.py pre_build.sh
echo "[*] You now have a shell!"
echo "[*] Please enter your exploit below (max 512 chars):"
read -n 512 cmd
exec su user1 -c "$cmd"
