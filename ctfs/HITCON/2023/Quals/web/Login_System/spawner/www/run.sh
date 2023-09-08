#!/bin/sh

if [ ! -e /var/run/docker.sock ]; then
    echo "[debug] docker daemon not found"
    exit 1
fi
if [ -z "$IMAGE_NAME" ]; then
    echo "[debug] IMAGE_NAME not found"
    exit 1
fi

echo "[debug] Building image "$IMAGE_NAME""
docker build -t "$IMAGE_NAME" /image

NODE_ENV=production node app.js
