# docker build -t koeri-stock . && docker run -p 1337:1337 koeri-stock
FROM ubuntu:22.10

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update --fix-missing && apt-get upgrade -y
RUN apt-get install -y make socat

RUN echo "dd0ddeaf2293dd418123b8fb03022337d7ac6ac3  /lib/x86_64-linux-gnu/libc.so.6" | sha1sum -c

RUN adduser --disabled-password --gecos "" user

WORKDIR /home/user/

COPY main main
COPY flag.txt flag.txt

# Set the ownership and permissions of the binary and flag file
RUN chown root:root /home/user/main && \
    chmod 555 /home/user/main && \
    chown root:root /home/user/flag.txt && \
    chmod 444 /home/user/flag.txt

EXPOSE 1337
USER user

ENTRYPOINT [ "socat", "-v", "tcp-listen:1337,reuseaddr,fork", "EXEC:'./main'" ]
