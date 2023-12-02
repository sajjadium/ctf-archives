FROM php:7.2-apache


RUN apt-get update && apt-get install -y libfreetype6-dev zlib1g-dev libpng-dev libonig-dev libjpeg-dev \
    && docker-php-ext-install mysqli pdo pdo_mysql \
    && docker-php-ext-enable mysqli pdo pdo_mysql 

RUN docker-php-ext-configure gd --with-freetype-dir=/usr/include/ --with-jpeg-dir=/usr/include/ && docker-php-ext-install gd

RUN service apache2 restart

COPY src /var/www/html
RUN chown -R www-data:www-data /var/www/html