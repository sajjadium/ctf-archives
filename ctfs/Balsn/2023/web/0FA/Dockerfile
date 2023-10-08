FROM ubuntu:18.04
ENV DEBIAN_FRONTEND=noninteractive

RUN apt update
RUN apt install -y git make gcc zlib1g-dev libpcre3-dev

ARG OPENSSL_VERSION=OpenSSL_1_1_1-stable
ARG NGINX_VERSION=release-1.23.1

WORKDIR /build

RUN mkdir logs
RUN git clone -b ${OPENSSL_VERSION} --depth=1 https://github.com/openssl/openssl && \
    git clone -b ${NGINX_VERSION} --depth=1 https://github.com/nginx/nginx

ADD patches/ /build/nginx-ssl-fingerprint/patches/
ADD src/ /build/nginx-ssl-fingerprint/src/
ADD conf/config /build/nginx-ssl-fingerprint/
ADD conf/nginx.conf /build/nginx/conf/

RUN patch -p1 -d openssl < nginx-ssl-fingerprint/patches/openssl.1_1_1.patch && \
    patch -p1 -d nginx < nginx-ssl-fingerprint/patches/nginx.patch && \
    cd nginx && \
    ASAN_OPTIONS=symbolize=1 ./auto/configure --with-openssl=$(pwd)/../openssl --add-module=$(pwd)/../nginx-ssl-fingerprint --with-http_ssl_module --with-stream_ssl_module --with-debug --with-stream --with-cc-opt="-fsanitize=address -O -fno-omit-frame-pointer" --with-ld-opt="-L/usr/local/lib -Wl,-E -lasan" && \
    make

RUN apt install php7.2-fpm -y
RUN apt install -y openssl

ADD conf/php.ini /etc/php/7.2/fpm/php.ini
ADD conf/www.conf /etc/php/7.2/fpm/pool.d/www.conf

ADD index.php /var/www/html/index.php
ADD config.php /var/www/html/config.php
ADD flag.php /var/www/html/flag.php
ADD conf/nginx.crt /build/nginx/ssl/nginx.crt
ADD conf/nginx.key /build/nginx/ssl/nginx.key

EXPOSE 8787
CMD /etc/init.d/php7.2-fpm start && ./nginx/objs/nginx -p /build -c nginx/conf/nginx.conf && tail -f /var/log/nginx.log
