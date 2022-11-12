#!/bin/bash
docker build --no-cache --tag=nosanbox .
docker run -p 1337:1337 --name=nosanbox --rm nosanbox