#!/bin/bash
docker rm -f web_drunken_bathrobe
docker build -t web_drunken_bathrobe . && \
docker run --name=web_drunken_bathrobe --rm -p1337:1337 -it web_drunken_bathrobe
