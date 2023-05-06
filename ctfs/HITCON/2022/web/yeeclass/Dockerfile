FROM php:8-apache

ARG TURNSTILE_SECRETKEY
ARG TURNSTILE_SITEKEY

RUN if [ -n "$TURNSTILE_SECRETKEY" ]; \
    then echo "SetEnv TURNSTILE_SECRETKEY ${TURNSTILE_SECRETKEY}" > /etc/apache2/conf-enabled/environment.conf; \
    fi
RUN if [ -n "$TURNSTILE_SITEKEY" ]; \
    then echo "SetEnv TURNSTILE_SITEKEY ${TURNSTILE_SITEKEY}" >> /etc/apache2/conf-enabled/environment.conf; \
    fi

RUN docker-php-ext-install pdo_mysql

USER www-data

COPY --chown=www-data:www-data ./src/ /var/www/html/

COPY --chown=www-data:www-data ./files/init.php /tmp

WORKDIR /var/www/html