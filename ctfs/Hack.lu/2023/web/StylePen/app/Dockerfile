FROM php:8.2-apache

RUN apt-get update -y && apt-get install -y libxml2-dev  && rm -rf /var/lib/apt/lists/*
RUN docker-php-ext-install xml
RUN mv "$PHP_INI_DIR/php.ini-production" "$PHP_INI_DIR/php.ini"

RUN a2enmod headers
COPY app.conf /etc/apache2/sites-available/000-default.conf

COPY src/ /var/www/html/
RUN sed -i 's/-1===l.*length)/true/' /var/www/html/static/widget.module.min.js