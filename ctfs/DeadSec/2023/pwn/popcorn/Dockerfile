FROM ubuntu:20.04

RUN apt update && apt install -y socat
RUN ln -s /flag.txt /flag


COPY popcorn /
COPY flag.txt /

EXPOSE 9001

CMD while sleep 1;do socat TCP-LISTEN:9001,reuseaddr,fork EXEC:/popcorn ;done
