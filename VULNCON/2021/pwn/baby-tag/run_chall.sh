#!/bin/sh

if [ "$#" -ne 1 ];
then
	printf "%b" "Usage:\n\t./run_chall.sh <PORT_TO_BE_EXPOSED>\n"
	exit 1
fi

docker build -t baby-tag .
docker run -d -p $1:1024 --rm -it baby-tag
