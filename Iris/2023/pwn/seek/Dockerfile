FROM ubuntu:20.04

RUN apt-get update && apt-get install -y gdb

COPY chal /home
COPY chal.c /home
CMD ["gdb", "/home/chal", "-ex", "dir /home"]
