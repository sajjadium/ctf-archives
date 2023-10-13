#!/bin/sh

docker run --rm --user "$(id -u)":"$(id -g)" -v "$PWD":/usr/src/rustymix -w /usr/src/rustymix rust:1.72.1 make clean all