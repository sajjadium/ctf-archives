FROM ubuntu:20.04

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

WORKDIR /app
COPY chall.c Makefile ./
RUN apt-get update && apt-get install -y musl musl-tools && \
make

# Challenge config starts here

FROM ubuntu:20.04

COPY --from=0 /usr/bin/nsjail /usr/bin/

RUN apt-get update && \
apt-get install -y libprotobuf17 libnl-route-3-200 musl && \
rm -rf /var/lib/apt/lists/*

RUN useradd -m ctf && \
mkdir /chroot/ && \
chown root:ctf /chroot && \
chmod 770 /chroot

WORKDIR /home/ctf/app
COPY --from=0 /app/chall /home/ctf/app
COPY flag.txt ./
COPY jail.cfg run.sh /

RUN chown -R root:ctf . && \
chmod 440 flag.txt

CMD /run.sh
