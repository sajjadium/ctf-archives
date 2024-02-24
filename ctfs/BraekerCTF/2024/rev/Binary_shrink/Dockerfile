FROM ubuntu:latest

RUN useradd -m ctf
WORKDIR /home/ctf

COPY ./binary_shrink .

ENTRYPOINT ./binary_shrink