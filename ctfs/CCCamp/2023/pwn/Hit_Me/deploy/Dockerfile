FROM ubuntu@sha256:a02c32cf0c2a7e8743c74deef66637aa70e063c9bd40e9e1f8c0b3ea0750b0ba

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update --fix-missing
RUN apt-get install -y socat

WORKDIR /root
COPY flag.txt flag.txt
COPY hit_me hit_me

EXPOSE 1024

ENTRYPOINT [ "socat", "tcp-l:1024,reuseaddr,fork", "EXEC:'./hit_me'" ]
