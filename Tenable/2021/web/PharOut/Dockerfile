FROM ubuntu
run apt update
RUN DEBIAN_FRONTEND=noninteractive apt install -y --no-install-recommends apache2 php7.4
RUN rm -rf /var/lib/apt/lists/*
RUN apt clean

COPY ./ports.conf /etc/apache2/ports.conf
COPY ./php.ini /etc/php/7.4/apache2/php.ini 
COPY . /var/www/html

ENV FLAG=not_the_flag
RUN cd /var/www/html && rm *.conf php.ini Dockerfile && chown www-data:www-data uploads && chmod o-rwx uploads
RUN rm /var/www/html/index.html

EXPOSE 8080
CMD ["apache2ctl", "-D", "FOREGROUND"]
