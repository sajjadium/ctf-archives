#!/bin/bash

docker build -t pg-build . \
    && id=$(docker create pg-build) \
    && docker cp $id:/opt/postgres - | gzip > postgres-binary.tar.gz \
    && docker rm -v $id
