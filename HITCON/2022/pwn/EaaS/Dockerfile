FROM ubuntu:20.04
MAINTAINER Lys

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -yq xinetd python3.8=3.8.10-0ubuntu1~20.04.5 python3-pip

RUN useradd -m eaas
RUN chown -R root:root /home/eaas
RUN chmod -R 755 /home/eaas

WORKDIR /
RUN pip3 install PyMuPDF==1.20.2

COPY readflag /
COPY flag /
COPY clear.cron /

RUN chown 0:0 readflag flag
RUN chmod 400 flag
RUN chmod +x readflag
RUN chmod +s readflag
RUN crontab clear.cron
RUN /etc/init.d/cron start

CMD ["/usr/sbin/xinetd","-dontfork"]
