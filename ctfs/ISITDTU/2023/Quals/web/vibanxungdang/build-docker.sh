#!/bin/bash
docker rm -f deser
docker rmi -f deser
docker build --tag=deser .
docker run -p 1337:1337 --name=deser deser