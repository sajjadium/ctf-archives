#! /bin/sh

DOCKER_BUILDKIT=1 docker build -t "qemu_building" .

docker run \
  -it \
  --mount type=bind,source="$(pwd)"/qemu,target=/qemu \
  --log-driver=none -a stdin -a stdout -a stderr qemu_building