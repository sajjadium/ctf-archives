#!/bin/bash
DIR="$(dirname "$(readlink -f "$0")")"

git clone https://github.com/contiki-ng/contiki-ng
git -C contiki-ng checkout release/v4.2

echo "applying patches"
git -C contiki-ng apply "$DIR/contiki.patch"

docker pull contiker/contiki-ng

export CNG_PATH="$(pwd)/contiki-ng"
docker run --privileged --sysctl net.ipv6.conf.all.disable_ipv6=0 --mount type=bind,source=$CNG_PATH,destination=/home/user/contiki-ng -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -v /dev/bus/usb:/dev/bus/usb -ti contiker/contiki-ng /bin/bash -c 'cd examples/rpl-border-router && make TARGET=native'

echo "Newly built binary in contiki-ng/examples/rpl-border-router/border-router.native"