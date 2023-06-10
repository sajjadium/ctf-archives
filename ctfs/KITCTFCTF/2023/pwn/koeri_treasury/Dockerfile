# docker build -t koeri-treasury . && docker run -p 1337:1337 koeri-treasury
FROM ubuntu:22.10

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update --fix-missing && apt-get upgrade -y
RUN apt-get install -y make socat

RUN adduser --disabled-password --gecos "" user

WORKDIR /home/user/

COPY main main
COPY libkoeri_crypt.so libkoeri_crypt.so

# Set the ownership and permissions of the binary and flag file
RUN chown root:root /home/user/main && chmod 555 /home/user/main

EXPOSE 1337
USER user

ENTRYPOINT [ "socat", "tcp-listen:1337,reuseaddr,fork", "EXEC:'./main'" ]
