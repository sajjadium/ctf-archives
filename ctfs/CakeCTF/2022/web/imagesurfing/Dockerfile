FROM php:8-apache

ADD flag.txt /
RUN chmod 444 /flag.txt

RUN apt update
RUN apt-get install -y libfreetype6-dev libjpeg62-turbo-dev libpng-dev \
    && docker-php-ext-install gd

WORKDIR /var/www/html

ADD index.php ./
RUN chown -R root:www-data ./
RUN chmod -R 440           ./
RUN chmod    550           ./
