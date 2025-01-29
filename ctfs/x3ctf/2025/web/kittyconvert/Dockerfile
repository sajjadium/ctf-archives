FROM php:8.4-apache

RUN apt-get update && apt-get install -y libpng-dev
RUN docker-php-ext-install gd && docker-php-ext-enable gd

COPY ./flag.txt /flag.txt
COPY src/ /var/www/html/
RUN chown www-data:www-data -R /var/www/html/uploads/
