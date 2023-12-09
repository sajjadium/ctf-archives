FROM ubuntu:22.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -y update --fix-missing && apt-get -y upgrade
RUN apt-get -y install python3 python3-pip

RUN mkdir /var/www
WORKDIR /var/www
COPY ./ ./

RUN pip3 install -r requirements.txt

ENV LANG C.UTF-8

RUN chmod 755 -R /var/www
RUN adduser -u 1000 execpy
RUN rm -rf /bin/*
USER execpy

CMD ["uwsgi", "--ini", "/var/www/uwsgi.ini"]