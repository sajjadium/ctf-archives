# Running locally:
# 1) echo 'hxp{FLAG}' > flag.txt
# 2) docker build -t counter .
# 3) docker run -p 8008:80 --rm -it counter

FROM debian:bullseye

RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    apt-get install -y \
        nginx \
        php-fpm \
    && rm -rf /var/lib/apt/lists/

RUN rm -rf /var/www/html/*
COPY docker-stuff/default /etc/nginx/sites-enabled/default
COPY docker-stuff/www.conf /etc/php/7.4/fpm/pool.d/www.conf

#  # Permission
#  7 rwx
#  6 rw-
#  5 r-x
#  4 r--
#  3 -wx
#  2 -w-
#  1 --x
#  0 ---

COPY flag.txt docker-stuff/readflag /
RUN chown 0:1337 /flag.txt /readflag && \
    chmod 040 /flag.txt && \
    chmod 2555 /readflag

COPY index.php /var/www/html/
RUN chown -R root:root /var/www && \
    find /var/www -type d -exec chmod 555 {} \; && \
    find /var/www -type f -exec chmod 444 {} \; && \
    chown -R root:root /tmp /var/tmp /var/lib/php/sessions && \
    chmod -R 000 /tmp /var/tmp /var/lib/php/sessions && \
    mkdir /var/www/html/data && \
    chmod 703 /var/www/html/data

RUN ln -sf /dev/null /var/log/nginx/access.log && \
    ln -sf /dev/null /var/log/nginx/error.log

RUN find / -ignore_readdir_race -type f \( -perm -4000 -o -perm -2000 \) -not -wholename /readflag -delete
USER www-data
RUN (find --version && id --version && sed --version && grep --version) > /dev/null
RUN ! find / -writable -or -user $(id -un) -or -group $(id -Gn|sed -e 's/ / -or -group /g') 2> /dev/null | grep -Ev -m 1 '^(/dev/|/run/|/proc/|/sys/|/var/lock|/var/log/nginx/error.log|/var/log/nginx/access.log|/var/www/html/data)'
USER root

EXPOSE 80
CMD while true; do find /var/www/html/data/ -mindepth 1 -mmin +15 -delete; sleep 1m; done & \
    /etc/init.d/php7.4-fpm start && \
    nginx -g 'daemon off;'
