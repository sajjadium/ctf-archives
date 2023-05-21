FROM php:7.3-apache

RUN apt -y update \
  && apt install -y \
  mariadb-client

# pdo_mysql package
RUN docker-php-ext-install mysqli

