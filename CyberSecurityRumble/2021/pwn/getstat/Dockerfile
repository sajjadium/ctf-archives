FROM ubuntu:20.04

COPY . /app

WORKDIR /app

RUN apt-get update && apt-get install -y socat
RUN useradd -UM chall

CMD /app/start.sh
