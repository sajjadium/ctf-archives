FROM ubuntu:20.04 as chroot

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get -y update && apt-get install -y \
    autoconf \
    bison \
    flex \
    gcc \
    g++ \
    git \
    libprotobuf-dev \
    libnl-route-3-dev \
    libseccomp-dev \
    libtool \
    make \
    pkg-config \
    protobuf-compiler

COPY nsjail/ /nsjail/

RUN cd /nsjail && make && mv /nsjail/nsjail /bin && rm -rf -- /nsjail

RUN apt-get install -y python3-dev
RUN apt-get install -y binutils-gold

COPY main /home/user/main
COPY flag.txt /home/user/flag.txt
COPY run.sh /home/user/run.sh

CMD nsjail -Mo --port 5000 --chroot / --user 99999 --group 99999 --use_cgroupv2 -- /home/user/run.sh
