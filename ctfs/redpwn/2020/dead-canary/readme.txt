To run on localhost:1337 with the current directory mounted at /ctf,

tar xf dead-canary.tar.gz && echo fake_flag > bin/flag.txt && docker run -v ${PWD}:/ctf --cap-add=SYS_PTRACE --rm --name redpwnctf-dead-canary -itp 1337:9999 $(docker build -q .)

You can get a shell with,

docker exec -it redpwnctf-dead-canary bash

We've also provided a simple install script to help setup an environment quickly.

apt-get update && apt-get install -qy curl && curl https://raw.githubusercontent.com/redpwn/dockerfiles/master/quick-install.sh | sh

