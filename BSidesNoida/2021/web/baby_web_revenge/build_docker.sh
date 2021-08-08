#!/bin/bash
docker rm -f web
docker build -t web . && \
docker run -d --name=web --rm -p80:80 -it web
