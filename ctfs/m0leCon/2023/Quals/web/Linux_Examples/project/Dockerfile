FROM php:8-cli

RUN curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/bin --filename=composer

RUN apt-get update && apt-get install -y git zip unzip libzip-dev iproute2 procps
RUN docker-php-ext-install zip

WORKDIR /app
COPY . .

RUN composer install

EXPOSE 8000
RUN cp .env.example .env
RUN php artisan key:generate

RUN chmod -R 555 /app
RUN chmod -R 777 /app/storage
RUN groupadd -r laravel && useradd -r -g laravel -s /sbin/nologin laravel
USER laravel

CMD php artisan serve --host 0.0.0.0
