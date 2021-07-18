#!/usr/bin/env bash

set -Eeuxo pipefail

HASH=5fb79a3b2deb3cf3f3e215b042e367ff067b7cb52b935b15995d7a1a1afc0fbea4ea99d8b2530282f3a7f85f2a457fa75afcf76a5976aba61c6e2d48b06c0b48

if ! sha512sum --status -c <(echo "${HASH}  docker.tar.gz"); then
    rm docker.tar.gz 2>/dev/null || true
    wget "https://storage.googleapis.com/gctf-2021-attachments-project/${HASH}" -O docker.tar.gz
    zcat docker.tar.gz | docker load
fi

docker run --privileged -p 127.0.0.1:1337:1337/tcp --rm -it pcivault-player-image
