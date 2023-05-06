#!/bin/bash
docker rm -f lemonthinker
docker build --tag=lemonthinker . && \
docker run -p 1337:1337 --restart=on-failure --name=lemonthinker --detach lemonthinker
