#!/bin/bash

if [ ! -f "./flag" ]; then
    echo "irisctf{fakeflag}" > ./flag
fi

docker build -t serious-banking .
echo "[+] Starting container (0.0.0.0:1024)"
docker run --rm --mount "type=bind,src=$(pwd)/flag,dst=/flag" --cap-add SYS_ADMIN --security-opt apparmor=unconfined -p 1024:1024 -ti serious-banking
