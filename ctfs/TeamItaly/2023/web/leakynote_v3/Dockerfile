FROM alpine:latest

RUN adduser -D -u 1000 -g 1000 -s /bin/sh www && mkdir /opt/admin_bot

RUN apk add --no-cache --update php81-fpm php81-pdo php81-pdo_sqlite php81-session supervisor nginx php-curl


COPY config/fpm.conf /etc/php81/php-fpm.d/www.conf
COPY config/supervisord.conf /etc/supervisord.conf
COPY config/nginx.conf /etc/nginx/nginx.conf
COPY config/php.ini /etc/php81/php.ini

COPY app /www

RUN chown -R www:www /var/lib/nginx

EXPOSE 1337

CMD /usr/bin/supervisord -c /etc/supervisord.conf