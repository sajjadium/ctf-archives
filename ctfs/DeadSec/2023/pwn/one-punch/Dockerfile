FROM ubuntu:22.04

COPY one_punch /

COPY flag.txt /

RUN apt update && apt install -y socat

EXPOSE 9001

CMD (while sleep 1;do socat TCP-LISTEN:9001,reuseaddr,fork EXEC:/one_punch ;done) 

