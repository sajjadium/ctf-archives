FROM ubuntu:22.04

RUN apt-get update && apt-get install -y socat
RUN useradd -UM chall

COPY . /app

WORKDIR /app

CMD /app/socat.sh
