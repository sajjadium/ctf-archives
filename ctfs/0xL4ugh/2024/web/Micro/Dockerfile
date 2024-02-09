FROM php:8.2-apache

RUN apt-get update && apt -y install mariadb-server && apt-get install -y libpng-dev python3 python3-pip libfontconfig nano
RUN docker-php-ext-install mysqli
COPY src /var/www/html/
COPY app.py /
RUN pip3 install pip==22.3.1 --break-system-packages
RUN pip3 install  mysql-connector-python flask
COPY init.sh /
COPY init.db /
RUN chmod +x /init.sh
EXPOSE 80
ENTRYPOINT [ "/bin/bash", "/init.sh"]
