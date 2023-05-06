#!/bin/sh
docker run --user $(id -u):$(id -g) --mount type=bind,source=$(pwd),target=/build -w /build --rm -i -t rust:1.64 /bin/sh