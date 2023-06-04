FROM buildpack-deps:bionic-scm AS builder

WORKDIR /tmp

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      g++ gcc libc6-dev make pkg-config
RUN apt-get install -y libssl-dev

RUN wget -q https://curl.haxx.se/download/curl-7.87.0.tar.gz && \
    tar xzf curl-7.87.0.tar.gz

WORKDIR /tmp/curl-7.87.0

RUN ./configure --prefix=/build \
      --disable-shared --enable-static --with-openssl \
      --disable-dict --disable-file --disable-ftps --disable-gopher \
      --disable-imap --disable-imaps --disable-ldap \
      --disable-ldaps --disable-pop3 --disable-pop3s --disable-rtmp --disable-rtsp \
      --disable-scp --disable-sftp --disable-smb --disable-smbs --disable-smtp \
      --disable-smtps --disable-telnet --disable-tftp && \
    make && \
    make install

FROM node:19-slim

COPY --from=builder /build/bin/curl /usr/sbin/curl

RUN apt-get update && \
  apt-get install -y ca-certificates && \
  rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY package.json ./
COPY static ./static
RUN npm i
COPY app.js .

RUN useradd -ms /bin/bash user
USER user

CMD ["/bin/sh", "-c", "while true; do node app.js; done"]