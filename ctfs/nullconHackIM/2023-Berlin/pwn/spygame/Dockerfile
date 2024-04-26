FROM ubuntu@sha256:c985bc3f77946b8e92c9a3648c6f31751a7dd972e06604785e47303f4ad47c4c

RUN apt update && apt install -y socat python3 python3-pip

RUN mkdir /app
COPY *.py *.c /app
WORKDIR /app
RUN python3 setup.py install

EXPOSE 9090
CMD ["socat", "TCP-LiSTEN:9090,FORK", "SYSTEM:'python3 game.py',user=nobody,group=nogroup"]
