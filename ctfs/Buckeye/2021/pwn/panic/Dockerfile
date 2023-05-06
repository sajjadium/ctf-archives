from rust:1.55 as builder

WORKDIR /challenge
COPY . .

# Yes, we are running a debug build
RUN cargo build

from ubuntu:20.04

# Install nsjail

ENV DEBIAN_FRONTEND=noninteractive

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
uidmap

RUN git clone https://github.com/google/nsjail --branch 3.0 && \
cd nsjail && \
make -j8 && \
mv nsjail /bin && \
cd / && \
rm -rf nsjail

WORKDIR /challenge

RUN useradd -m ctf && \
mkdir /chroot/ && \
chown root:ctf /chroot && \
chmod 770 /chroot

COPY flag.txt ./
COPY jail.cfg run.sh /
COPY --from=builder /challenge/target/debug/panic /challenge/panic

RUN chown -R root:ctf . && \
chmod 440 flag.txt

CMD /run.sh

