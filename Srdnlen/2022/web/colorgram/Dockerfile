# Install mysqli to make php interact with mysql
FROM php:8.1.1-apache

# Install zip
RUN apt-get update && apt-get install -y \
    zip \
    unzip 

# Install mysqli
RUN docker-php-ext-install mysqli && docker-php-ext-enable mysqli

RUN cd /var/www/html

# Install composer
RUN php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');"
RUN php -r "if (hash_file('sha384', 'composer-setup.php') === '55ce33d7678c5a611085589f1f3ddf8b3c52d662cd01d4ba75c0ee0459970c2200a51f492d557530c71c15d8dba01eae') { echo 'Installer verified'; } else { echo 'Installer corrupt'; unlink('composer-setup.php'); } echo PHP_EOL;"
RUN php composer-setup.php
RUN php -r "unlink('composer-setup.php');"
RUN mv ./composer.phar /usr/local/bin/composer

# Install php-jwt
RUN composer require firebase/php-jwt
RUN composer install

# Add db initialization schema
ADD db/init.sql /docker-entrypoint-initdb.d/
