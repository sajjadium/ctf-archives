FROM ubuntu:22.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -y update --fix-missing && apt-get -y upgrade
RUN apt-get -y install python3 \
                       python3-pip \
                       libgtk-3-0 \
                       libnss3 \
                       libnspr4 \
                       libdrm2 \
                       libgbm1 \
                       libasound2

RUN mkdir /var/www
WORKDIR /var/www
COPY ./ ./

RUN pip3 install -r requirements.txt
RUN playwright install

ENV LANG C.UTF-8

CMD ["uwsgi", "--ini", "/var/www/uwsgi.ini"]