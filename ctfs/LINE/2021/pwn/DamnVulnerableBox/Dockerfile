FROM ubuntu:20.04

ENV DEBIAN_FRONTEND noninteractive

WORKDIR /
RUN apt-get update -y && apt-get upgrade -y
RUN apt-get -y install software-properties-common locales poppler-utils --fix-missing

RUN apt-get update --fix-missing -y && apt-get -y --fix-missing dist-upgrade && apt-get -y upgrade --fix-missing && apt-get -q -y install xinetd lib32z1 libextractor3 net-tools netcat sudo curl wget python3 python3-pip clang 
RUN useradd ctf -s /usr/sbin/nologin

ADD start.sh /
ADD ctf /etc/xinetd.d/

ADD box /

RUN chmod a+x /box
RUN chmod a+x /start.sh

ADD flag /flag

CMD ["/bin/dash", "-c", "/start.sh"]

EXPOSE 9999

