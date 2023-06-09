# docker build -t seccomp-sandbox . && docker run -p 1337:1337 seccomp-sandbox

FROM ubuntu:22.04

RUN apt update \
    && apt install -y --no-install-recommends gcc libc6-dev libseccomp-dev socat \
    && rm -rf /var/lib/apt/lists/*

COPY flag.txt /flag.txt

WORKDIR /src
COPY sandbox.c ./
RUN gcc -o sandbox sandbox.c -lseccomp

RUN useradd ctf
USER ctf

ENTRYPOINT [ "socat", "tcp-listen:1337,reuseaddr", "EXEC:./sandbox,pty,ctty,setsid,stderr,sigint,sane" ]
