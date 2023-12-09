FROM php:8.2.12-apache-bullseye
COPY --from=composer:2.6.5 /usr/bin/composer /usr/bin/composer
COPY php/composer.json /var/www
COPY php/composer.lock /var/www
RUN apt-get update && apt-get install -y unzip && cd /var/www && composer install

COPY php/public/* /var/www/html
COPY php/* /var/www
