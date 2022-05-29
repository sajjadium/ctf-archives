#!/bin/bash

if [ -z "$(docker images -q constricted-challenge:dist)" ]; then
    docker build . -t constricted-challenge:dist
fi

ARGS=$@
if [ -f "$1" ]; then
    INPUT_PATH="/input/$(basename $1)";
    MOUNT="-v $(realpath $1):$INPUT_PATH";
    shift;
    ARGS="$INPUT_PATH $@";
fi

docker run $MOUNT --rm -it constricted-challenge:dist /challenge/boa $ARGS
