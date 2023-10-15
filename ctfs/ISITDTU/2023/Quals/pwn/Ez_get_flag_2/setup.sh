#!/bin/sh
#

docker build -t "challenge" . --network=host && docker run -d -p "0.0.0.0:3000:3000" --cap-add=SYS_PTRACE challenge