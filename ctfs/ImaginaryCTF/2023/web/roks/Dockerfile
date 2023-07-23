FROM php:8-apache

RUN /usr/sbin/useradd -u 1000 user

COPY index.php /var/www/html/
COPY file.php /var/www/html/
COPY styles.css /var/www/html/
COPY stopHacking.png /var/www/html/

RUN mkdir /var/www/html/images
COPY images/* /var/www/html/images
COPY flag.png /

VOLUME /var/log/apache2
VOLUME /var/run/apache2

CMD bash -c 'source /etc/apache2/envvars && APACHE_RUN_USER=user APACHE_RUN_GROUP=user /usr/sbin/apache2 -D FOREGROUND'


