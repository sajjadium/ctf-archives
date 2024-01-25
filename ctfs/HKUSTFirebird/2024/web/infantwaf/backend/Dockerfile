FROM php:8.3.1-apache

RUN apt update && DEBIAN_FRONTEND=noninteractive && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /var/www/html

COPY index.php ./

USER www-data