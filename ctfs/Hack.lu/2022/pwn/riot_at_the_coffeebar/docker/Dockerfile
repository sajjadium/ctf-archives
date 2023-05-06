FROM ubuntu:20.04

# Install main dependencies and some useful tools
RUN apt-get update && \
    apt-get install -y --no-install-recommends ca-certificates wget socat && rm -rf /var/lib/apt/lists/*

ARG RENODE_VERSION=1.13.0

# Install Renode
RUN wget https://github.com/renode/renode/releases/download/v${RENODE_VERSION}/renode_${RENODE_VERSION}_amd64.deb && \
    apt-get update && \
    apt-get install -y --no-install-recommends ./renode_${RENODE_VERSION}_amd64.deb python3-dev && \
    rm ./renode_${RENODE_VERSION}_amd64.deb && \
    rm -rf /var/lib/apt/lists/*
RUN pip3 install -r /opt/renode/tests/requirements.txt --no-cache-dir

# add challenge user
RUN useradd -ms /bin/bash challuser
USER challuser
WORKDIR /home/challuser

# add challenge files
ADD coffe.py socat.sh chall.sh chall-debug.sh chall.resc chall-debug.resc gnrc_networking.elf ./

ENV PORT=1337
EXPOSE 1337
CMD ./socat.sh
