#!/bin/bash

docker build . -t secure-wallet
docker run --rm --init -it secure-wallet
