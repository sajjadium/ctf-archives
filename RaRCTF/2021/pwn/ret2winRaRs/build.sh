#!/bin/bash
docker rm -f ret2winrars
docker build --tag=ret2winrars . && \
docker run -p 1337:1337 --restart=on-failure --name=ret2winrars --detach ret2winrars

