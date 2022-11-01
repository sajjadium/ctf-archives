FROM php:8-apache

ARG RANDOM_ID
ENV RANDOM_ID $RANDOM_ID

COPY src/ /var/www/html/

RUN mkdir -p /var/www/html/uploads/$RANDOM_ID/
COPY flag.gif /var/www/html/uploads/$RANDOM_ID/
RUN chown www-data:www-data -R /var/www/html/uploads
RUN chmod 700 -R /var/www/html/uploads
RUN chmod 500 -R /var/www/html/uploads/$RANDOM_ID/

RUN mv "$PHP_INI_DIR/php.ini-production" "$PHP_INI_DIR/php.ini"
RUN apt-get update -y && apt-get install -y libpng-dev
RUN docker-php-ext-install gd
RUN docker-php-ext-install mysqli

RUN a2enmod headers
RUN a2enmod proxy
RUN a2enmod proxy_http
COPY yummygifs.conf /etc/apache2/sites-available/000-default.conf

