FROM ubuntu:20.04
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update
RUN apt-get install -y wget curl apache2 git php-gd php-mysql php

RUN git clone https://github.com/gnuboard/gnuboard5 /tmp/gnuboard
RUN cp -r /tmp/gnuboard/* /var/www/html
RUN sed -i 's/AllowOverride None/AllowOverride All/g' /etc/apache2/apache2.conf

WORKDIR /var/www/html

RUN mkdir data
RUN chmod 777 data
RUN rm -rf index.html /tmp/gnuboard

RUN echo '$flag = "hsctf{flag_will_be_here}";' >> /var/www/html/common.php

ADD entrypoint.sh /
CMD /entrypoint.sh
