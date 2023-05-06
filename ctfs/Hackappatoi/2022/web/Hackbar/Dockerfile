FROM php:8.1.12-fpm-alpine

EXPOSE 8000

# RUN docker-php-ext-install pdo pdo_mysql sockets
RUN curl -sS https://getcomposer.org/installer | php -- \
     --install-dir=/usr/local/bin --filename=composer
RUN apk add sqlite

COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

WORKDIR /app
COPY ./src .

RUN chmod 444 /app/flag

RUN chown -R www-data:www-data /app
RUN composer install
USER www-data

CMD [ "php", "artisan", "serve", "-vvv", "--host=0.0.0.0" ]