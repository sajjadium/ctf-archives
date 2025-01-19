FROM debian:12.8@sha256:10901ccd8d249047f9761845b4594f121edef079cfd8224edebd9ea726f0a7f6

RUN apt-get update && apt-get install -y \
        gcc=4:12.2.0-3 \
        make=4.3-4.1 \
        libssl-dev=3.0.15-1~deb12u1 \
        socat=1.7.4.4-2 \
        xxd=2:9.0.1378-2 \
        wget=1.21.3-1+b2 \
        xz-utils=5.4.1-0.2 \
        m4=1.4.19-3 \
    && apt-get clean

WORKDIR /app

RUN wget https://gmplib.org/download/gmp/gmp-6.3.0.tar.xz && \
    tar -xf /app/gmp-6.3.0.tar.xz && \
    rm /app/gmp-6.3.0.tar.xz

WORKDIR /app/gmp-6.3.0

RUN ./configure && \
    make && \
    make install


RUN useradd ctf

WORKDIR /app

COPY --chown=root:ctf --chmod=050 ./build/cryptopwn ./cryptopwn
COPY --chown=root:ctf --chmod=040 ./flag.txt ./flag.txt

USER ctf

EXPOSE 1337

ENTRYPOINT ["socat", "-t", "180", "-T", "30", "TCP-LISTEN:1337,reuseaddr,nodelay,fork", "EXEC:/app/cryptopwn,stderr"]
