# Running locally:
# 1) echo 'hxp{FLAG}' > flag.txt
# 2) docker build -t shitty_blog .
# 3) docker run -p 8888:80 --rm -it shitty_blog

FROM debian:bullseye

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        nginx \
        php-fpm \
        php-sqlite3 \
    && rm -rf /var/lib/apt/lists/

RUN rm -rf /var/www/html/*
COPY docker-stuff/default /etc/nginx/sites-enabled/default
COPY docker-stuff/www.conf /etc/php/7.4/fpm/pool.d/www.conf

COPY flag.txt docker-stuff/readflag /
RUN chown 0:1337 /flag.txt /readflag && \
    chmod 040 /flag.txt && \
    chmod 2555 /readflag

COPY index.php favicon.png /var/www/html/
RUN chown -R root:root /var/www && \
    find /var/www -type d -exec chmod 555 {} \; && \
    find /var/www -type f -exec chmod 444 {} \; && \
    chown -R root:root /tmp /var/tmp /var/lib/php/sessions && \
    chmod -R 000 /tmp /var/tmp /var/lib/php/sessions && \
    mkdir -p /var/www/html/data && \
    chmod 703 /var/www/html/data && \
    sed -i "s/SECRET_PLACEHOLDER/$(< /dev/urandom tr -dc a-zA-Z0-9 | head -c 24)/g" /var/www/html/index.php

RUN ln -sf /dev/stdout /var/log/nginx/access.log && \
    ln -sf /dev/stderr /var/log/nginx/error.log

RUN find / -ignore_readdir_race -type f \( -perm -4000 -o -perm -2000 \) -not -wholename /readflag -delete
USER www-data
RUN (find --version && id --version && sed --version && grep --version) > /dev/null
RUN ! find / -writable -or -user $(id -un) -or -group $(id -Gn|sed -e 's/ / -or -group /g') 2> /dev/null | grep -Ev -m 1 '^(/dev/|/run/|/proc/|/sys/|/var/lock|/var/log/nginx/error.log|/var/log/nginx/access.log|/var/www/html/data)'

USER root
EXPOSE 80
CMD while true; do find /var/www/html/data/ -mindepth 1 -mmin +15 -delete; sleep 1m; done & \
    /etc/init.d/php7.4-fpm start && \
    nginx -g 'daemon off;'

