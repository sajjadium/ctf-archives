#!/bin/bash

docker build . -t linectf_damn
docker run -it -d -p 10006:9999 --name linectf_damn linectf_damn
