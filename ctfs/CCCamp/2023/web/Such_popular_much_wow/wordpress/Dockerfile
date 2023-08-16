#
# NOTE: THIS DOCKERFILE IS GENERATED VIA "apply-templates.sh"
#
# PLEASE DO NOT EDIT IT DIRECTLY.
#

FROM php:8.1-apache
RUN docker-php-ext-install mysqli && docker-php-ext-enable mysqli

RUN apt-get update && apt-get upgrade -y

RUN cp /usr/local/etc/php/php.ini-production /usr/local/etc/php.ini && \
    sed -i "s/error_reporting = .*$/error_reporting = E_ERROR | E_WARNING | E_PARSE/"     /usr/local/etc/php.ini && \
    sed -i 's/Listen 80/Listen 1024/' /etc/apache2/ports.conf && \
    a2enmod rewrite && a2enmod headers


RUN apt-get update && apt-get install default-mysql-client firefox-esr python3 python3-pip wget tar -y
RUN pip3 install selenium requests --break-system-packages

WORKDIR /tmp
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux64.tar.gz
RUN tar -xvzf geckodriver-v0.33.0-linux64.tar.gz && rm geckodriver-v0.33.0-linux64.tar.gz && chmod +x geckodriver && cp geckodriver /usr/local/bin/

COPY 000-default.conf /etc/apache2/sites-enabled/000-default.conf 


COPY entry-point.sh /usr/bin/entry-point.sh
RUN chmod 777 /usr/bin/entry-point.sh
COPY firefox-script.py /usr/bin/firefox-script.py
RUN chmod 777 /usr/bin/firefox-script.py

RUn mkdir -p /var/www/.cache /var/www/.mozilla && chmod 777 /var/www/.cache /var/www/.mozilla

USER www-data
WORKDIR /var/www/html

COPY flag.txt /var/www/flag.txt

RUN curl https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar > /var/www/html/wp-cli.phar

RUN ls -al
ENTRYPOINT [ "/usr/bin/entry-point.sh" ]
