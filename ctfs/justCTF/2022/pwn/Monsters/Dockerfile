FROM ubuntu:21.10
#FROM disconnect3d/nsjail:3.1-6483728

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y libc++-dev libc++abi-dev socat clang make libunwind-dev

RUN groupadd ctf && \
    useradd -G ctf --home=/pwn pwn

WORKDIR /task

# If we want to build (note: sources are not available for participants)
#COPY ./src /task/src
#RUN cd /task/src && make && cp monsters /task/ && cd /task
COPY monsters .
COPY run.sh .

# Helper/fixer for socat issues
COPY socat-sigpipe-fixup /task/socat-sigpipe-fixup
RUN chmod 111 /task/socat-sigpipe-fixup && \
    chmod 700 /task/run.sh

CMD "/task/run.sh"

