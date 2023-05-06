#!/bin/sh
sudo docker build -f build.Dockerfile -t fnkbuild .

id="$(sudo docker create fnkbuild)"

sudo docker cp "$id:/root/main" ./fnk
sudo docker container rm "$id"

sudo chown "$(whoami):" ./fnk
