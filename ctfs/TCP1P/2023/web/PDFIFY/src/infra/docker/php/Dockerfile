FROM node:buster as node
FROM php:7.4-apache

# Apache port
EXPOSE 80

# Bot port
EXPOSE 5000

RUN apt-get update
RUN apt-get -y install git libicu-dev libonig-dev libzip-dev zip unzip locales && \
  apt-get -y install libpq-dev libxml2-dev libbz2-dev zlib1g-dev && \
  apt-get -y install libsqlite3-dev libsqlite3-0 mariadb-client curl exif ftp && \
  apt-get -y install wkhtmltopdf && \
  locale-gen en_US.UTF-8 && \
  localedef -f UTF-8 -i en_US en_US.UTF-8 && \
  a2enmod rewrite && \
  docker-php-ext-install intl pdo pdo_mysql mysqli zip bcmath
RUN apt-get -y install chromium
RUN apt-get -y install supervisor

# composer command
COPY --from=composer:2.0 /usr/bin/composer /usr/bin/composer
# node command
COPY --from=node /usr/local/bin /usr/local/bin
# npm command
COPY --from=node /usr/local/lib /usr/local/lib
# yarn command
COPY --from=node /opt /opt

COPY ./infra/docker/php/php.ini /usr/local/etc/php/php.ini
COPY ./infra/docker/apache/httpd.conf /etc/apache2/sites-available/000-default.conf

# bot
RUN useradd -m bot
USER bot
RUN mkdir /home/bot/app/
COPY ./bot/ /home/bot/app/

USER  root
# supervisord
COPY ./infra/docker/supervisord/* /etc/supervisor/conf.d/

# timezone environment
ENV TZ=UTC \
  # locale
  LANG=en_US.UTF-8 \
  LANGUAGE=en_US:en \
  LC_ALL=en_US.UTF-8 \
  # composer environment
  COMPOSER_ALLOW_SUPERUSER=1 \
  COMPOSER_HOME=/composer

RUN composer config -g process-timeout 3600 && \
  composer config -g repos.packagist composer https://packagist.org

WORKDIR /work/backend

RUN apt-get clean

COPY ./backend .
RUN chown www-data:www-data ./writable -R

CMD ["sh", "-c", "supervisord -n"]
