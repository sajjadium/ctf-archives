#! /bin/sh

DOCKER_BUILDKIT=1 docker build -t "edk2_building" .

docker run \
  -it \
  --mount type=bind,source="$(pwd)"/edk2,target=/build \
  --log-driver=none -a stdin -a stdout -a stderr edk2_building