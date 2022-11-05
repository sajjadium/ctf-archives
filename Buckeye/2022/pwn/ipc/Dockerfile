# glibc 2.31
FROM ubuntu:20.04@sha256:b25ef49a40b7797937d0d23eca3b0a41701af6757afca23d504d50826f0b37ce

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
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/google/nsjail.git
RUN cd /nsjail && make && mv /nsjail/nsjail /bin && rm -rf -- /nsjail

RUN apt-get update && \
apt-get install -y \
gcc uidmap netcat && \
rm -rf /var/lib/apt/lists/* && \
useradd -m ctf && \
mkdir -p /home/ctf/challenge/

RUN mkdir /chroot/ && \
chown root:ctf /chroot && \
chmod 770 /chroot

COPY ./ /home/ctf/challenge/src/

WORKDIR /home/ctf/challenge/src/
RUN rm -f server/server flag-client/flag_client
RUN make && cp server/server flag-client/flag_client start.sh flag.txt ../


WORKDIR /home/ctf/challenge/

# Create n00b user (part 1)
RUN useradd -m n00b -G ctf

# Create server user (part 2)
RUN useradd -m server -G n00b,ctf && \
chown server:server server && \
chmod 500 server 

# Create flag user (part 3)
RUN useradd -m flag -G ctf && \
chown flag:flag flag_client && \
chmod 500 flag_client && \
chown flag:flag flag.txt && \
chmod 400 flag.txt

RUN mv src/jail.cfg src/nsjail.sh / && \
rm -rf src/

EXPOSE 1337
ENTRYPOINT ["/nsjail.sh"]
