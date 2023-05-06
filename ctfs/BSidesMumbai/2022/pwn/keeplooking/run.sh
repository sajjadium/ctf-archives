#!/bin/sh

if [ "$#" -ne 1 ];
then
	printf "%b" "Usage:\n\t./run_chall.sh <PORT_TO_BE_EXPOSED>\n"
	exit 1
fi

docker build -t pwn3 .
docker run -d -p $1:1337 --rm -it pwn3
