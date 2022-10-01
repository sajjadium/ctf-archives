#!/bin/bash

docker build -t pwn_gets:latest .
docker run -it --rm -d --name=gets -p1337:1337 pwn_gets:latest
