FROM php:8-apache
RUN docker-php-ext-install pdo pdo_mysql
COPY src /var/www/html

RUN a2enmod ssl && a2enmod rewrite
RUN mkdir -p /etc/apache2/ssl

COPY ./ssl/*.pem /etc/apache2/ssl/
COPY ./000-default.conf /etc/apache2/sites-available/000-default.conf
