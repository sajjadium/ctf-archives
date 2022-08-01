FROM ubuntu:22.10

RUN apt-get update -yyq && apt-get upgrade -yyq
RUN apt install socat -yyq
RUN apt-get install -y \
    autoconf \
    bison \
    flex \
    gcc \
    git \
    g++ \
    git \
    libprotobuf-dev \
    libnl-route-3-dev \
    libtool \
    make \
    pkg-config \
    protobuf-compiler \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -M -s /bin/false ctf
RUN mkdir /tmp/nsjail && cd /tmp/nsjail && git clone https://github.com/google/nsjail && cd nsjail && make && mv nsjail /bin && rm -rf -- /nsjail
COPY entrypoint.sh /tmp/
RUN chmod 555 /tmp/entrypoint.sh
COPY main flag.txt /var/service/
USER ctf

ENTRYPOINT /tmp/entrypoint.sh 