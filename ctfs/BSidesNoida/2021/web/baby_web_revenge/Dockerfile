FROM debian:buster-slim

RUN useradd www

RUN apt-get update && apt-get install -y supervisor nginx lsb-release curl wget

RUN wget -O /etc/apt/trusted.gpg.d/php.gpg https://packages.sury.org/php/apt.gpg
RUN echo "deb https://packages.sury.org/php/ $(lsb_release -sc) main" | tee /etc/apt/sources.list.d/php.list

RUN apt update && apt install -y php7.4-fpm

RUN apt install php7.4-sqlite3 -y 
COPY config/fpm.conf /etc/php/7.4/fpm/php-fpm.conf
COPY config/supervisord.conf /etc/supervisord.conf
COPY config/ctf.conf /etc/nginx/nginx.conf

# Copy challenge files
COPY index.php /www/
COPY karma.db /www/
COPY download.jpeg /www/
COPY error.html /www/

# Setup permissions
RUN chown -R www:www /www /var/lib/nginx

EXPOSE 80

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]
