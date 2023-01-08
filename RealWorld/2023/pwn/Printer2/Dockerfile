FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -qy cups 

COPY ./flag /flag
COPY ./cupsd.conf /etc/cups/cupsd.conf
COPY ./start.sh /start.sh

RUN chmod 755 /flag
RUN chmod 755 /start.sh

ENTRYPOINT ["/start.sh"]

