#!/bin/sh
docker container rm -f miss-analyzer
docker run -d -p7273:7273 --restart=always --name=miss-analyzer --privileged miss-analyzer