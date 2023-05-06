FROM ubuntu:18.04

RUN apt-get update && apt-get install -y socat

CMD echo 1 > /proc/sys/kernel/randomize_va_space

RUN useradd -m -s /bin/bash user

USER user

COPY tourniquet /home/user/
COPY flag.txt /home/user

CMD cd /home/user && socat TCP-LISTEN:10901,reuseaddr,fork EXEC:/home/user/tourniquet
