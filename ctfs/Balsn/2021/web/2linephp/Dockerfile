FROM php:7.4.11-apache

RUN sed -i 's/deb.debian.org/mirror.sjtu.edu.cn/g' /etc/apt/sources.list && \
    sed -i 's/security.debian.org/mirror.sjtu.edu.cn/g' /etc/apt/sources.list && \
    apt-get update -y && \
    apt-get install gcc -y 
#   docker-php-ext-install zip && \

COPY source /var/www/html
COPY flag /flag

RUN chmod 600 /flag
ADD readflag.c /readflag.c
RUN gcc /readflag.c -o /readflag && \
chmod +s /readflag

RUN chmod -R 544 /var/www/html/
