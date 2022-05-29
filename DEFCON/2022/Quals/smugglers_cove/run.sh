#!/bin/bash
if [[ $# -eq 0 ]] ; then
    echo './run.sh <lua file>'
    exit 1
fi

FILE=$(basename $1)
LUA_PATH=/$(head -c10 /dev/urandom | xxd -p)/$FILE

if [ -z "$(docker images -q smugglers-cove)" ]; then
    docker build . -t smugglers-cove
fi
docker run -v $(realpath $1):$LUA_PATH --rm -it smugglers-cove $LUA_PATH
