# echo 'hxp{FLAG}' > flag.txt && docker build -t security-scanner . && docker run --cap-add=SYS_ADMIN --security-opt apparmor=unconfined -ti -p 8010:80 security-scanner

FROM debian:buster

RUN DEBIAN_FRONTEND=noninteractive apt-get update && \
    apt-get install -y \
        ca-certificates \
        git \
        memcached \
        nginx \
        php-fpm \
        php-memcached  \
    && rm -rf /var/lib/apt/lists/

RUN rm -rf /var/www/html/*
COPY docker-stuff/default /etc/nginx/sites-enabled/default
COPY docker-stuff/www.conf /etc/php/7.3/fpm/pool.d/www.conf

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
    find /var/www -type f -exec chmod 444 {} \;

RUN ln -sf /dev/stdout /var/log/nginx/access.log && \
    ln -sf /dev/stderr /var/log/nginx/error.log

USER www-data
RUN (find --version && id --version && sed --version && grep --version) > /dev/null
RUN ! find / -writable -or -user $(id -un) -or -group $(id -Gn|sed -e 's/ / -or -group /g') 2> /dev/null | grep -Ev -m 1 '^(/dev/|/run/|/proc/|/sys/|/tmp|/var/tmp|/var/lock|/var/log/nginx/error.log|/var/log/nginx/access.log|/var/lib/php/sessions)'

USER root
EXPOSE 80
CMD /etc/init.d/php7.3-fpm start && \
    /etc/init.d/memcached start && \
    nginx -g 'daemon off;'
