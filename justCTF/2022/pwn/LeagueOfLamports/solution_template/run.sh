#!/usr/bin/env sh

if [ "$#" -ne 2 ]; then
    echo "Use: <host> <port>"
    exit 1
fi

IMAGE_NAME=solver
HOST=$1
PORT=$2

docker build \
        -t $IMAGE_NAME \
        -f Dockerfile \
        .

docker rm -f $IMAGE_NAME
docker run \
    --network="host" \
    --name $IMAGE_NAME \
    $IMAGE_NAME \
    /tmp/solver/solve.py HOST=$HOST PORT=$PORT
