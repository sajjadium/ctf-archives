FROM ubuntu as chroot

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
    protobuf-compiler \
    curl \
    build-essential \
    ca-certificates \
    python3 \
    python3-dev \
    python3-pip \
    python3-venv \
    binutils-gold

COPY nsjail/ /nsjail/

RUN cd /nsjail && make && mv /nsjail/nsjail /bin && rm -rf -- /nsjail

RUN python3 -m venv /home/user/venv
RUN /home/user/venv/bin/pip install --upgrade pip setuptools wheel

COPY requirements.txt /home/user/requirements.txt
RUN /home/user/venv/bin/pip install -r /home/user/requirements.txt

COPY pow.py /home/user/pow.py
COPY main /home/user/main
COPY libc-2.24.so /home/user/libc-2.24.so
COPY ld-2.24.so /home/user/ld-2.24.so
COPY flag.txt /home/user/flag.txt
COPY run.sh /home/user/run.sh

RUN ln -s /home/user/libc-2.24.so /home/user/libc.so.6

CMD nsjail -Mo --port 5000 --chroot / --user 99999 --group 99999 --max_conns_per_ip 1 --use_cgroupv2 -- /home/user/run.sh
