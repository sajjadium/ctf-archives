FROM php:8-apache

RUN apt update && apt install -y \
        libfreetype6-dev \
        libjpeg62-turbo-dev \
        libpng-dev \
        git \
        libonig-dev \
    && docker-php-ext-configure gd --with-freetype --with-jpeg \
    && docker-php-ext-install -j$(nproc) gd \
    && docker-php-ext-install mbstring

COPY --from=composer/composer /usr/bin/composer /usr/bin/composer
RUN cd /var/www/ && composer require mpdf/mpdf
RUN chmod -R 733 /var/www/vendor/mpdf/mpdf/tmp