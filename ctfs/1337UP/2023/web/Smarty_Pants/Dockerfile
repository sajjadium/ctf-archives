FROM php:7.4.33-apache-bullseye
RUN apt-get update -y && apt-get install -y git zlib1g-dev libzip-dev zip unzip && rm -rf /var/lib/apt
RUN docker-php-ext-configure zip
RUN docker-php-ext-install zip

WORKDIR /var/www/
COPY --from=composer:latest /usr/bin/composer /usr/local/bin/composer
RUN composer require smarty/smarty
COPY index.php index.tpl /var/www/html/
COPY flag.txt start.sh /
EXPOSE 80
CMD ["sh","/start.sh"]