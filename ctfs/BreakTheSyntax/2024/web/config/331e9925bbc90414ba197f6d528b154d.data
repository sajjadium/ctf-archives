FROM trafex/php-nginx:3.5.0

RUN rm -r /var/www/html/*
COPY app/. /var/www/html

COPY config/nginx.conf /etc/nginx/nginx.conf
COPY config/default.conf /etc/nginx/conf.d/default.conf
COPY config/php.ini /etc/php83/php.ini

RUN mkdir -p /var/www/html/examples
COPY config/php.ini /var/www/html/examples/php.ini

COPY flag /flag

USER root
RUN FLAG_DIR=$(cat /proc/sys/kernel/random/uuid) && mkdir /$FLAG_DIR && mv /flag /$FLAG_DIR/flag
USER nobody

EXPOSE 8000

RUN mkdir /var/www/html/uploads
