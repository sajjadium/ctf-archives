FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y apache2 && a2enmod cgi
ADD ./site.conf /etc/apache2/sites-available/site.conf
RUN a2ensite site && a2dissite 000-default
ADD ./cee_gee_eye.cgi /app/cee_gee_eye.cgi
RUN chmod -R 755 /app

CMD apachectl -DFOREGROUND
