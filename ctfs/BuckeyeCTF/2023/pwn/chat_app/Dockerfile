FROM rust:1.70@sha256:b9331b83517a41d3c0d5dceb4ac83f3fc2c1b6d9781d8284d783ba04a7efd9ca as build

RUN rustup target add x86_64-unknown-linux-gnu
RUN rustup toolchain install 1.70-x86_64-unknown-linux-gnu

COPY server/ /app/server
COPY client/ /app/client
COPY common/ /app/common

WORKDIR /app/server
RUN cargo build --target x86_64-unknown-linux-gnu --release
RUN mkdir /app/bin && cp target/x86_64-unknown-linux-gnu/release/server /app/bin/server

WORKDIR /app/client
RUN cargo build --target x86_64-unknown-linux-gnu --release
RUN cp target/x86_64-unknown-linux-gnu/release/client /app/bin/client

FROM ubuntu:22.04@sha256:b492494d8e0113c4ad3fe4528a4b5ff89faa5331f7d52c5c138196f69ce176a6

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
RUN cd /nsjail && git checkout 3.3 && make && mv /nsjail/nsjail /bin && rm -rf -- /nsjail

RUN apt-get update && \
apt-get install -y \
gcc uidmap netcat cmake && \
rm -rf /var/lib/apt/lists/* && \
useradd -m ctf && \
mkdir -p /home/ctf/bins

# venv for POW
RUN python3 -m venv /venv
RUN bash -c "source /venv/bin/activate && pip3 install ecdsa requests proxy-protocol==0.7.5"

# setup chroot
RUN mkdir /chroot/ && \
chown root:ctf /chroot && \
chmod 770 /chroot

# copy bins, instancer source, and flags
COPY --from=build /app/bin/server /app/bin/client /home/ctf/bins/
COPY instancer/ /home/ctf/instancer/
COPY flag-client.txt /home/ctf/

WORKDIR /home/ctf/

# fix perms
RUN rm -rf src/ && \
chown -R root:ctf . && \
chmod 550 bins/server bins/client && \
chown root:ctf / /home /home/ctf/ && \
chmod 440 flag-client.txt && \
chmod +x instancer/*.sh

EXPOSE 9000
WORKDIR /home/ctf/instancer/
CMD ["./setup.sh"]
