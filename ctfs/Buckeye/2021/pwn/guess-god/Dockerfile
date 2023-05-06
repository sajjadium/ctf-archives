FROM ubuntu:21.04@sha256:e082dd99faca91acb1f43347bf8b50ac9b9d2fdcc72253e29fe65b6b1eb1445d

ENV DEBIAN_FRONTEND=noninteractive

# Install nsjail
RUN apt-get -y update && apt-get install -y \
    autoconf \
    bison \
    flex \
    gcc \
    g++ \
    git \
    libprotobuf-dev \
    libnl-route-3-dev \
    libtool \
    make \
    pkg-config \
    protobuf-compiler \
    uidmap \
    cmake \
    iptables \
    net-tools \
    iproute2 \
    python3-venv \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/google/nsjail.git
RUN cd /nsjail && make && mv /nsjail/nsjail /bin && rm -rf -- /nsjail

RUN apt-get update && \
apt-get install -y \
gcc uidmap netcat cmake && \
rm -rf /var/lib/apt/lists/* && \
useradd -m ctf && \
mkdir -p /home/ctf/challenge/

RUN mkdir /chroot/ && \
chown root:ctf /chroot && \
chmod 770 /chroot

# Install oatpp
RUN git clone https://github.com/oatpp/oatpp.git
RUN cd /oatpp && git checkout 1.2.5 && mkdir build && cd build && cmake .. && make install

COPY ./ /home/ctf/challenge/src/

WORKDIR /home/ctf/challenge/src/
RUN mkdir -p src/build && cd src/build && cmake .. && make
RUN cp src/build/flag_server-exe src/build/libkylezip.so flag.txt /home/ctf/challenge/


WORKDIR /home/ctf/challenge/

RUN mv src/jail.cfg src/server.py src/pow.py src/setup.sh src/nsjail.sh / && \
rm -rf src/ && \
chown -R root:ctf . && \
chmod 550 flag_server-exe && \
chown root:ctf / /home /home/ctf/ && \
chmod 440 flag.txt


# venv for POW
RUN python3 -m venv /venv
RUN bash -c "source /venv/bin/activate && pip3 install ecdsa requests proxy-protocol"


EXPOSE 9000
CMD ["/setup.sh"]
