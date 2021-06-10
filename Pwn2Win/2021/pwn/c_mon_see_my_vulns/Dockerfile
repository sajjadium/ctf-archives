FROM php:8.0.2-apache

WORKDIR /opt

# Setup readflag binary
COPY ./readflag.c readflag.c
RUN gcc readflag.c -o readflag && chmod 4777 readflag && rm readflag.c

# Copy flag
COPY flag.txt /root/flag.txt

# Copy source code
COPY --chown=www-data:www-data src /var/www/html/

# Install extension
COPY csvparser.so /usr/local/lib/php/extensions/no-debug-non-zts-20200930/csvparser.so

# copy php config file
COPY config/php.ini /usr/local/etc/php/

# setup reverse proxy
RUN apt update && apt -y install nginx
COPY config/proxy.conf /etc/nginx/sites-available/proxy.conf
RUN rm /etc/nginx/sites-enabled/default && ln -s /etc/nginx/sites-available/proxy.conf /etc/nginx/sites-enabled/proxy.conf

# Expose reverse proxy port
#EXPOSE 1337

# Entrypoint
COPY entrypoint.sh .
ENTRYPOINT ["/opt/entrypoint.sh"]
