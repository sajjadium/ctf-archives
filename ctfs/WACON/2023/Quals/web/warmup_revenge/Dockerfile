FROM php:7.4-apache

RUN apt-get update && apt-get upgrade -y && apt-get install python3 -y

RUN docker-php-ext-install mysqli
RUN docker-php-ext-install sockets

RUN rm -rf /var/www/html/
COPY ./html /var/www/html/

RUN chmod 777 /var/www/html/upload/

EXPOSE 80