#!/bin/bash

docker build . -t proxy-viewer
docker run -p1337:1337 proxy-viewer