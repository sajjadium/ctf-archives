FROM php:7.4-fpm

RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list &&\
    apt-get update

COPY html /var/www/html
COPY flag /flag
COPY readflag where_is_your_gift
COPY jsonparser.so /usr/local/lib/php/extensions/no-debug-non-zts-20190902/jsonparser.so

RUN chmod 400 /flag &&\
    chmod 4111 where_is_your_gift &&\
    chmod -R 555 /var/www/html &&\
    echo "extension=/usr/local/lib/php/extensions/no-debug-non-zts-20190902/jsonparser.so" > /usr/local/etc/php/conf.d/jsonparser.ini