FROM ubuntu:latest

MAINTAINER anonymous
RUN apt-get update
RUN apt-get install xinetd systemctl -y

RUN useradd -m mailclient
RUN useradd -m mailserver

RUN mkdir -p /home/mailserver/data
RUN mkdir -p /home/mailserver/data/users
RUN mkdir -p /tmp/mail/
RUN mkdir -p /tmp/mail/content

COPY ./mailserver /home/mailserver/mailserver
COPY ./mailclient /home/mailclient/mailclient
COPY ./shares/flag /home/mailclient/flag
COPY ./shares/mailclient /etc/xinetd.d/mailclient
COPY ./shares/mailserver.service /etc/systemd/system/
COPY ./shares/init.sh /init.sh

RUN chown -R root:mailserver /home/mailserver/
RUN chown -R root:mailclient /home/mailclient/

RUN chmod -R 750 /home/mailserver/
RUN chmod -R 750 /home/mailclient/
RUN chown -R 755 /tmp/mail/
RUN chmod -R 777 /tmp/mail/content/
RUN chmod -R 770 /home/mailserver/data

RUN systemctl daemon-reload
RUN chmod +x /init.sh

WORKDIR /

CMD ["/init.sh"]

EXPOSE 8080