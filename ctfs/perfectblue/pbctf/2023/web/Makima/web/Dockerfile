FROM debian:bullseye

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        nginx \
        php7.4-fpm \
        php7.4-gd \
    && rm -rf /var/lib/apt/lists/

# nginx + fastcgi
RUN rm -rf /var/www/html/*
COPY nginx/default.conf /etc/nginx/sites-enabled/default
COPY nginx/www.conf /etc/php/7.4/fpm/pool.d/www.conf

RUN ln -sf /dev/stdout /var/log/nginx/access.log && \
    ln -sf /dev/stderr /var/log/nginx/error.log

# php
RUN mkdir -p /var/www/html/uploads && \
    chmod 703 /var/www/html/uploads

COPY php/uploads/makima.png /var/www/html/uploads/makima.png
COPY php/index.php /var/www/html/index.php

COPY flag.txt /flag

USER root
EXPOSE 8080

CMD /etc/init.d/php7.4-fpm start && \
    nginx -g 'daemon off;'
