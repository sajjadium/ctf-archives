#!/bin/bash

NAME="multi-auth"

cd private

docker build -t ${NAME} .

docker rm -f ${NAME}
docker run -d \
    --restart=always \
    --name=${NAME} \
    --privileged \
    -p 1337:7331 \
    ${NAME}
