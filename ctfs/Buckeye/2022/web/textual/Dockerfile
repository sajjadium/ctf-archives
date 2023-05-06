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
uidmap \
&& \
rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/google/nsjail --branch 3.0 && \
cd nsjail && \
make -j8 && \
mv nsjail /bin && \
cd / && \
rm -rf nsjail

# Challenge config starts here

FROM node:bullseye

ENV DEBIAN_FRONTEND=noninteractive
COPY --from=0 /usr/bin/nsjail /usr/bin/

RUN useradd -m ctf && \
mkdir /chroot/ && \
chown root:ctf /chroot && \
chmod 770 /chroot

# install lyx
RUN apt-get update
RUN apt-get install -y texlive-base pandoc

WORKDIR /home/ctf/app
COPY package* ./
RUN npm i
RUN cp /bin/sh /bin/sh-orig
COPY . ./

RUN chown -R root:ctf . && \
chmod 440 flag.tex 
RUN chmod +x run.sh

CMD ./run.sh