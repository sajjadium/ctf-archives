FROM php:8-apache-bullseye


RUN apt-get update && apt-get install -y \
    libfreetype6-dev \
    libjpeg62-turbo-dev \
    libpng-dev \
    git

# install php gd extension, jpeg
RUN docker-php-ext-install -j$(nproc) iconv \
    && docker-php-ext-configure gd --with-freetype --with-jpeg \
    && docker-php-ext-install -j$(nproc) gd

# install memcached extension
RUN apt-get install -y libz-dev libmemcached-dev 
RUN pecl install memcached && docker-php-ext-enable memcached

COPY webapp/ /var/www/meme-maker/
ENV APACHE_DOCUMENT_ROOT /var/www/meme-maker/public

RUN sed -ri -e 's!/var/www/html!${APACHE_DOCUMENT_ROOT}!g' /etc/apache2/sites-available/*.conf
RUN sed -ri -e 's!/var/www/!${APACHE_DOCUMENT_ROOT}!g' /etc/apache2/apache2.conf /etc/apache2/conf-available/*.conf
RUN a2enmod rewrite

WORKDIR /var/www/meme-maker

# install composer
COPY --from=composer/composer /usr/bin/composer /usr/bin/composer
RUN composer install --no-dev --no-interaction --optimize-autoloader --no-cache


RUN chown -R www-data:www-data storage
RUN chown -R www-data:www-data public/generated
RUN chown -R www-data:www-data bootstrap/cache

RUN php artisan key:generate
RUN sed -i 's/APP_DEBUG=true/APP_DEBUG=false/g' .env

RUN echo "BA1SN{fake}" > /flag
RUN chmod 0400 /flag
COPY readflag.c /readflag.c
RUN gcc /readflag.c -o /readflag
RUN chmod 4755 /readflag

