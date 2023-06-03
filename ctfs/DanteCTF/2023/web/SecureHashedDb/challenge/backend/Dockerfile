FROM php:7.4-apache

WORKDIR /srv/app

# Install php dependencies
RUN apt-get -y update && \
    apt-get -y install unzip sqlite3 && \
    rm -rf /var/cache/apt/archives /var/lib/apt/lists/*

# Install composer dependencies
COPY --from=composer:latest /usr/bin/composer /usr/local/bin/composer
RUN mkdir -p /var/www/html/utils && \
    cd /var/www/html/utils && \
    composer require miladrahimi/php-jwt "2.*"

# Set-up globally writable dir
RUN mkdir /srv/app/container &&\
    chown -R www-data:www-data /srv/app/container

# Set-up sqlite db
COPY hashes.db dbs/
COPY dbPopulate.sh ./
RUN chmod +x ./dbPopulate.sh && \
    ./dbPopulate.sh && \
    rm ./dbPopulate.sh && \
    chmod -R 777 ./dbs

# Copy src
COPY ./src /var/www/html
COPY flag.txt /flag.txt
COPY apache2.conf /etc/apache2/apache2.conf
COPY ports.conf /etc/apache2/ports.conf
# Update apache + set flag permissions
RUN a2enmod rewrite && \
    chown root:root /flag.txt && \
    chmod 444 /flag.txt

EXPOSE 1717
