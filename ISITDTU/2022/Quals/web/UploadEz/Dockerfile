FROM php:7.0-apache

COPY 000-default.conf /etc/apache2/sites-available/

COPY php.ini /usr/local/etc/php/

COPY flag /flag

COPY index.php /var/www/html/index.php

WORKDIR /var/www/html/
