#!/bin/bash
set -ex

# Build hitcon2022_sandbox docker first
pushd chrome_docker
docker-compose build
popd

export PORT=8080
export WWW="$(pwd)/www"
export UNAME=$(uname)

mkdir -p "$WWW" || true
tar xf ./mojo_bindings.tar.xz -C "$WWW"

# npm install -g node-static
(cd "$WWW" && static -a 0.0.0.0 -p $PORT) &

if [ "$UNAME" == "Linux" ]; then
  export HOST_IP=$(ip route | grep docker0 | awk '{print $9}')
fi

socat tcp-listen:30263,fork,reuseaddr,bind=0.0.0.0 exec:"./run.sh"
