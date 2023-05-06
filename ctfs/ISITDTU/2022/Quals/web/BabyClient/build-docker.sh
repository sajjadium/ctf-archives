#!/bin/bash
docker build --tag=baby_client .
docker run -d -p 9000:9000 -it --name=baby_client baby_client