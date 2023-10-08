FROM ubuntu:20.04
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update
RUN apt-get dist-upgrade -y
RUN apt-get install apache2 -y
RUN apt-get install net-tools curl iputils-ping -y
RUN ln -s /etc/apache2/mods-available/cgi.load /etc/apache2/mods-enabled/cgi.load
COPY 000-default.conf /etc/apache2/sites-enabled/
COPY index.html /var/www/html
COPY nier.jpg /var/www/html
COPY spread.cgi /usr/lib/cgi-bin
RUN chmod -R 755 /usr/lib/cgi-bin
RUN a2enmod cgid
RUN service apache2 restart
CMD ["/usr/sbin/apachectl", "-D", "FOREGROUND"]

