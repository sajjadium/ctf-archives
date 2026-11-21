#!/bin/sh

ENGINE=podman
if ! [ -x "$(command -v podman)" ]; then
  ENGINE=docker
  if ! [ -x "$(command -v docker)" ]; then
    echo "[!] Please install a container engine such as podman or docker."
    exit 1
  fi
fi

$ENGINE build -t glacier-military-daemon .
$ENGINE run -it \
  --log-driver=none \
  --env PWD=/home/sci33098 \
  --read-only-tmpfs=true \
  --restart no \
  --uts=private \
  --pull never \
  --read-only \
  --no-hosts \
  --network none \
  --memory 5m \
  --user sci33098 \
  --hostname pmclab006 \
  --rm localhost/glacier-military-daemon:latest \
  /bin/zsh
  #--timeout=300
