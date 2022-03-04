#!/bin/sh
./build.sh
sudo docker build -t fnk .
sudo docker run --add-host host.docker.internal:host-gateway --rm -p1447:1447 -it fnk
