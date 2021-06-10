FROM ubuntu:18.04

RUN apt update && apt -y upgrade

RUN apt update
RUN apt -y install apache2 python3-pip
RUN pip3 install elasticsearch
COPY ./apache/000-default.conf /etc/apache2/sites-available/000-default.conf
RUN a2enmod http2
RUN a2enmod cgi
RUN a2dismod status
RUN echo 'Listen 8080'>/etc/apache2/ports.conf


COPY ./apache/entrypoint /entrypoint
COPY ./apache/elastic_init.py /elastic_init.py
RUN chmod +x /entrypoint
ENTRYPOINT ["/entrypoint"]

#RUN service apache2 reload
CMD ["/usr/sbin/apache2ctl", "-DFOREGROUND"]