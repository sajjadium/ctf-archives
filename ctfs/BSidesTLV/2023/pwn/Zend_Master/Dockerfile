FROM gcc:13.1 AS build

ARG PHP_VERSION=8.1.19
WORKDIR /usr/src/app
COPY pwn1.patch pwn2.patch ./

RUN set -eux; \
    \
    apt-get update; \
    apt-get install -y curl tar file autoconf bison re2c; \
    \
    # Download PHP source
    curl -Lo /usr/src/app/php-${PHP_VERSION}.tar.gz \
            https://github.com/php/php-src/archive/refs/tags/php-${PHP_VERSION}.tar.gz; \
    tar -xf /usr/src/app/php-${PHP_VERSION}.tar.gz; \
    \
    # Build PHP
    cd /usr/src/app/php-src-php-${PHP_VERSION}; \
    patch -p0 -i /usr/src/app/pwn1.patch; \
    patch -p0 -i /usr/src/app/pwn2.patch; \
    ./buildconf --force; \
    ./configure --prefix=/usr/local/php --enable-cli --disable-all --enable-opcache --enable-opcache-jit; \
    make -j$(nproc); \
    make install

FROM python:3.11-slim

ARG USERNAME=app
WORKDIR /usr/src/app

ENV IDLE_TIMEOUT=30
ENV SESSION_TIMEOUT=120
ENV COMMAND="python /usr/src/app/server.py"
ENV PROCESS_OPTIONS="pty,setuid=${USERNAME},echo=0,raw,iexten=0"
ENV ADDRESS_OPTIONS="fork,reuseaddr"

COPY --from=build /usr/local/php /usr/local/php
RUN set -eux; \
    \
    apt-get update; \
    apt-get install -y socat; \
    \
    ln -s /usr/local/php/bin/php /usr/local/bin/php; \
    adduser --disabled-password --no-create-home --gecos ${USERNAME} ${USERNAME}

COPY conf.ini server.py flag.txt sanity-tests.py /usr/src/app/

USER ${USERNAME}
ENV HOME=/tmp

EXPOSE 1337
CMD [ "sh", "-c", "socat -dd -T${IDLE_TIMEOUT} \"TCP4-LISTEN:1337,${ADDRESS_OPTIONS}\" \"EXEC:${COMMAND},${PROCESS_OPTIONS}\"" ]
