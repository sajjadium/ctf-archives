FROM magic_space_bus:static as binary

FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt -y update && apt -y upgrade && apt -y install \
    tini python3 python3-pip gdb git

RUN pip3 install pwntools
WORKDIR /challenge/ptools/
RUN git clone https://github.com/pwndbg/pwndbg.git && cd pwndbg && ./setup.sh
WORKDIR /challenge/
COPY malloc.c .

WORKDIR /challenge/
COPY run.sh /challenge/

COPY magic ./

# If you'd like to use your own copy of the challenge uncomment this line out
# This is the binary from the static container
# COPY --from=binary /magic/magic /challenge/

RUN chmod +x run.sh

# Add less privledged user and change to them
RUN groupadd -r --gid=1000 challenge && \
    useradd -m -r -s /bin/bash -g challenge --uid=1000 challenge && \
    chown -R 1000:1000 /challenge/

USER challenge

WORKDIR /challenge

ENTRYPOINT [ "tini", "--", "/challenge/run.sh" ]
