FROM ubuntu:20.04
RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y systemctl python3-pip libmnl0 libnetfilter-queue1 libnfnetlink0
RUN python3 -m pip install protobuf grpcio
COPY opensnitch_1.5.2-1_amd64.deb /
RUN dpkg -i /opensnitch_1.5.2-1_amd64.deb
RUN useradd -m test
COPY flag /
COPY run.sh /
