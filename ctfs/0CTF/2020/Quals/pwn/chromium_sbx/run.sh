#!/bin/bash

export PORT=8080
export WWW="$(pwd)/www"
export UNAME=$(uname)

mkdir $WWW || true

docker build -t mojo .
unzip -o mojo_js.zip -d $WWW

# npm install -g node-static
(cd $WWW && static -a 0.0.0.0 -p $PORT) &

if [ "$UNAME" == "Linux" ]; then
  export HOST_IP=$(ip route | grep docker0 | awk '{print $9}')
fi

# apt install socat
socat tcp-listen:1337,fork,reuseaddr,bind=0.0.0.0 exec:"python3 -u ./server.py"
