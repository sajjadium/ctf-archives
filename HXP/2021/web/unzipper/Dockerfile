# Running locally:
# 1) echo 'hxp{FLAG}' > flag.txt
# 2) docker build -t unzipper .
# 3) docker run -p 8200:80 --rm -it unzipper

FROM debian:bullseye

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        nginx php-fpm unzip && \
    rm -rf /var/lib/apt/lists/

RUN rm -rf /var/www/html/*
COPY docker-stuff/default /etc/nginx/sites-enabled/default
COPY docker-stuff/www.conf /etc/php/7.4/fpm/pool.d/www.conf
COPY docker-stuff/cleanup /usr/bin/cleanup

COPY flag.txt /
COPY index.php /var/www/html/
RUN chown -R root:root /var/www /flag.txt /usr/bin/cleanup && \
    chmod 004 /flag.txt && \
    chmod 500 /bin/su && \
    chmod 005 /usr/bin/cleanup && \
    find /var/www -type d -exec chmod 555 {} \; && \
    find /var/www -type f -exec chmod 444 {} \; && \
    mkdir -p /var/www/html/data && \
    chmod 703 /var/www/html/data

RUN ln -sf /dev/stdout /var/log/nginx/access.log && \
    ln -sf /dev/stderr /var/log/nginx/error.log

RUN find / -ignore_readdir_race -type f \( -perm -4000 -o -perm -2000 \) -not -wholename /readflag -delete
USER www-data
RUN (find --version && id --version && sed --version && grep --version) > /dev/null
RUN ! find / -writable -or -user $(id -un) -or -group $(id -Gn|sed -e 's/ / -or -group  /g') 2> /dev/null | grep -Ev -m 1 '^(/dev/|/run/|/proc/|/sys/|/tmp|/var/tmp|/var/lock|/var/log/nginx/error.log|/var/log/nginx/access.log|/var/lib/php/sessions|/var/www/html/data)'

USER root
EXPOSE 80
CMD while true; do find /var/www/html/data/ -maxdepth 1 -mindepth 1 -type d -mmin +1 -exec \
        /bin/su --shell=/usr/bin/cleanup -- www-data '{}' \; ; sleep 10s; done & \
    /etc/init.d/php7.4-fpm start && \
    nginx -g 'daemon off;'
