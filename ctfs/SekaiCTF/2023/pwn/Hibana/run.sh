#!/bin/bash
docker run \
    --rm \
    --mount type=bind,source="$(pwd)"/flag,target=/flag-$(cat /dev/urandom | tr -dc a-f0-9 | fold -w32 | head -n1),readonly \
    --mount type=bind,source="$(pwd)"/engine_i686.so,target=/home/steam/svends/engine_i686.so,readonly \
    --mount type=bind,source="$(pwd)"/addons,target=/home/steam/svends/svencoop/addons,readonly \
    --mount type=bind,source="$(pwd)"/headicons,target=/home/steam/svends/svencoop/headicons,readonly \
    --mount type=bind,source="$(pwd)"/server.cfg,target=/home/steam/svends/svencoop/server.cfg,readonly \
    --memory=128m \
    -p 8888:27015/udp \
    --env PASSWORD=$PASSWORD \
    --name hibana -it \
    hibana
