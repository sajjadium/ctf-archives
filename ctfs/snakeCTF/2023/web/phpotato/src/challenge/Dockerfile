FROM php:8-apache

RUN a2enmod rewrite
RUN docker-php-ext-install mysqli pdo pdo_mysql && docker-php-ext-enable pdo_mysql
COPY php.ini /usr/local/etc/php/php.ini
COPY src /var/www/html/
COPY .htaccess /var/www/html/ 