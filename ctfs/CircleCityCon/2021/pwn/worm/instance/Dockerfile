FROM ubuntu:20.04

RUN apt-get update && \
apt-get install -y gcc libcap2-bin python3 && \
rm -rf /var/lib/apt/lists/*

COPY . /

CMD timeout --foreground 300 /run.sh
